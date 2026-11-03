from flask import jsonify, request, send_file
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models.user import User
from app.services.bulk_pretriage_service import BulkPretriageService


class BulkPretriageController:
    def __init__(self):
        self.service = BulkPretriageService()

    @jwt_required()
    def evaluate_excel(self):
        try:
            try:
                id_user = int(get_jwt_identity())
            except (TypeError, ValueError):
                return jsonify({
                    "ok": False,
                    "message": "Token inválido."
                }), 401

            user = db.session.get(User, id_user)

            if (
                user is None
                or not user.is_active
                or user.role is None
                or user.role.name.lower() != "admin"
            ):
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

            filename = uploaded_file.filename.lower()
            if not filename.endswith(".xlsx"):
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

            result_bytes, statistics = self.service.process(file_bytes)

            response = send_file(
                __import__("io").BytesIO(result_bytes),
                mimetype=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                ),
                as_attachment=True,
                download_name="resultados_priorizacion_urgentia.xlsx",
            )

            response.headers["X-Casos-Procesados"] = str(statistics["procesados"])
            response.headers["X-Casos-Clasificados"] = str(statistics["clasificados"])
            response.headers["X-Casos-Revision"] = str(statistics["revision_clinica"])
            response.headers["X-Casos-Error"] = str(statistics["errores"])

            return response

        except ValueError as error:
            return jsonify({
                "ok": False,
                "message": str(error)
            }), 400

        except Exception:
            return jsonify({
                "ok": False,
                "message": "No fue posible procesar el Excel."
            }), 500
