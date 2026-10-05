from flask import request, jsonify

from app.services.pretriage_agent_service import PretriageAgentService


class PretriageAgentController:

    def __init__(self):
        self.service = PretriageAgentService()

    def evaluate(self):

        try:
            # 1. Obtener los datos enviados en la petición
            data = request.get_json(silent=True)

            if not data:
                return jsonify({
                    "ok": False,
                    "message": "No se recibieron datos"
                }), 400

            # 2. Obtener el ID del pretriaje
            id_pretriage = data.get("id_pretriage")

            if id_pretriage is None:
                return jsonify({
                    "ok": False,
                    "message": "El campo id_pretriage es obligatorio"
                }), 400

            # 3. Validar que el ID sea numérico
            try:
                id_pretriage = int(id_pretriage)

            except (TypeError, ValueError):
                return jsonify({
                    "ok": False,
                    "message": "El id_pretriage debe ser un número válido"
                }), 400

            # 4. Enviar solamente el ID al service
            # El service consulta la información del paciente
            # directamente desde la base de datos.
            result = self.service.evaluate(
                id_pretriage=id_pretriage
            )

            # 5. Devolver el resultado generado por la IA
            return jsonify({
                "ok": True,
                "id_pretriage": id_pretriage,
                "result": result
            }), 200

        except ValueError as e:
            return jsonify({
                "ok": False,
                "message": str(e)
            }), 400

        except Exception as e:
            return jsonify({
                "ok": False,
                "message": "Ocurrió un error al evaluar el pretriaje con IA",
                "detalle": str(e)
            }), 500