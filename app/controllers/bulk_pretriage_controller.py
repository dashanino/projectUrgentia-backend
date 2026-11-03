from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from threading import Lock
from uuid import uuid4

from flask import jsonify, request, send_file
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models.user import User
from app.services.bulk_pretriage_service import BulkPretriageService


class BulkPretriageController:
    """Controlador para evaluación masiva de casos con seguimiento de progreso."""

    _executor = ThreadPoolExecutor(max_workers=2)
    _jobs = {}
    _lock = Lock()

    def __init__(self):
        self.service = BulkPretriageService()

    @staticmethod
    def _is_admin():
        try:
            id_user = int(get_jwt_identity())
        except (TypeError, ValueError):
            return False, None

        user = db.session.get(User, id_user)
        is_admin = (
            user is not None
            and user.is_active
            and user.role is not None
            and user.role.name.lower() == "admin"
        )
        return is_admin, user

    def _run_job(self, job_id, file_bytes):
        def update_progress(progress):
            with self._lock:
                job = self._jobs.get(job_id)
                if job:
                    job["progress"] = progress

        try:
            result_bytes, statistics = self.service.process(
                file_bytes,
                progress_callback=update_progress,
            )

            with self._lock:
                self._jobs[job_id].update({
                    "status": "completed",
                    "progress": {
                        "status": "completado",
                        "current": statistics["procesados"],
                        "total": statistics["procesados"],
                        "row": None,
                        "percentage": 100,
                    },
                    "result": result_bytes,
                    "statistics": statistics,
                })
        except Exception as error:
            with self._lock:
                self._jobs[job_id].update({
                    "status": "error",
                    "error": str(error),
                })

    @jwt_required()
    def evaluate_excel(self):
        is_admin, _ = self._is_admin()
        if not is_admin:
            try:
                int(get_jwt_identity())
            except (TypeError, ValueError):
                return jsonify({"ok": False, "message": "Token inválido."}), 401
            return jsonify({
                "ok": False,
                "message": "Esta función es exclusiva para administradores."
            }), 403

        uploaded_file = request.files.get("file")
        if uploaded_file is None or not uploaded_file.filename:
            return jsonify({
                "ok": False,
                "message": "Debes seleccionar un archivo Excel."
            }), 400

        if not uploaded_file.filename.lower().endswith(".xlsx"):
            return jsonify({
                "ok": False,
                "message": "El archivo debe estar en formato .xlsx."
            }), 400

        file_bytes = uploaded_file.read()
        if not file_bytes:
            return jsonify({
                "ok": False,
                "message": "El archivo está vacío."
            }), 400

        if len(file_bytes) > 20 * 1024 * 1024:
            return jsonify({
                "ok": False,
                "message": "El archivo no puede superar 20 MB."
            }), 400

        job_id = str(uuid4())
        with self._lock:
            self._jobs[job_id] = {
                "status": "queued",
                "progress": {
                    "status": "en cola",
                    "current": 0,
                    "total": 0,
                    "row": None,
                    "percentage": 0,
                },
                "result": None,
                "statistics": None,
                "error": None,
            }

        self._executor.submit(self._run_job, job_id, file_bytes)

        return jsonify({
            "ok": True,
            "job_id": job_id,
        }), 202

    @jwt_required()
    def get_progress(self, job_id):
        is_admin, _ = self._is_admin()
        if not is_admin:
            return jsonify({
                "ok": False,
                "message": "Esta función es exclusiva para administradores."
            }), 403

        with self._lock:
            job = self._jobs.get(job_id)
            if job is None:
                return jsonify({
                    "ok": False,
                    "message": "No se encontró el procesamiento solicitado."
                }), 404

            return jsonify({
                "ok": True,
                "status": job["status"],
                "progress": job["progress"],
                "statistics": job["statistics"],
                "error": job["error"],
            })

    @jwt_required()
    def download_result(self, job_id):
        is_admin, _ = self._is_admin()
        if not is_admin:
            return jsonify({
                "ok": False,
                "message": "Esta función es exclusiva para administradores."
            }), 403

        with self._lock:
            job = self._jobs.get(job_id)
            if job is None:
                return jsonify({
                    "ok": False,
                    "message": "No se encontró el procesamiento solicitado."
                }), 404

            if job["status"] != "completed" or job["result"] is None:
                return jsonify({
                    "ok": False,
                    "message": "El procesamiento todavía no ha terminado."
                }), 409

            result_bytes = job["result"]

        return send_file(
            BytesIO(result_bytes),
            mimetype=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            ),
            as_attachment=True,
            download_name="resultados_priorizacion_urgentia.xlsx",
        )
