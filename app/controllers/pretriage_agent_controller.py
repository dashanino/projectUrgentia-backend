
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from app.services.pretriage_safety_service import revisar_seguridad_ia
from app.services.pretriage_agent_service import (
    PretriageAgentService,
    RevisionClinicaRequerida
)
from app.services.pregunta_ia_service import guardar_respuesta_ia, guardar_respuestas_ia
from app.services.pretriage_access_service import (
    validar_acceso_pretriage,
    validar_evaluacion_inicial
)
from app.extensions import db

class PretriageAgentController:

    def __init__(self):
        self.service = PretriageAgentService()

    # =========================================================
    # 1. EVALUACIÓN CON IA
    # =========================================================

    @jwt_required()
    def evaluate(self):

        try:
            data = request.get_json(silent=True)

            if not isinstance(data, dict):
                return jsonify({
                    "ok": False,
                    "message": "Debes enviar un objeto JSON"
                }), 400

            try:
                id_pretriage = int(data.get("id_pretriage"))
            except (TypeError, ValueError):
                return jsonify({
                    "ok": False,
                    "message": "El id_pretriage debe ser un número válido"
                }), 400

            # Verificar que el token corresponda al pretriage
            validar_acceso_pretriage(id_pretriage)
            # Verificar que las reglas fueron evaluadas y no existe alerta
            validar_evaluacion_inicial(
            id_pretriage,
            requerir_sintomas=True 
            )

            # Consultar la información y evaluar con IA
            result = self.service.evaluate(
                id_pretriage=id_pretriage
            )

            # Si la evaluación requiere más información, generar
            # el bloque de preguntas antes de responder al frontend.
            if result.get("accion") == "preguntas_adicionales":

                bloque = self.service.generate_additional_questions(
                    id_pretriage=id_pretriage
                )

                if bloque.get("accion") == "bloque_preguntas":
                    result["preguntas"] = bloque.get("preguntas", [])

                elif bloque.get("accion") == "pregunta_pendiente":
                    result["preguntas"] = [{
                        "id_pregunta": bloque["id_pregunta"],
                        "pregunta": bloque["pregunta"],
                        "orden": bloque["orden"]
                    }]

                else:
                    raise RevisionClinicaRequerida(
                        "No fue posible completar las preguntas adicionales. "
                        "Se requiere valoración por personal de salud."
                    )

                if not result.get("preguntas"):
                    raise RevisionClinicaRequerida(
                        "No se pudieron obtener preguntas clínicas adicionales."
                    )

            return jsonify({
                "ok": True,
                "id_pretriage": id_pretriage,
                "result": result
            }), 200

        except RevisionClinicaRequerida as e:
            return jsonify({
                "ok": True,
                "id_pretriage": id_pretriage,
                "accion": "revision_clinica",
                "prioridad": None,
                "message": str(e)
            }), 200
        except PermissionError as e:
            return jsonify({
                "ok": False,
                "message": str(e)
            }), 403

        except ValueError as e:
            return jsonify({
                "ok": False,
                "message": str(e)
            }), 400

        except Exception:
            return jsonify({
                "ok": False,
                "message": "Ocurrió un error al evaluar el pretriage con IA"
            }), 500

    # =========================================================
    # 2. GENERAR PREGUNTA DINÁMICA CON IA
    # =========================================================

    @jwt_required()
    def generar_pregunta(self):

        try:
            data = request.get_json(silent=True)

            if not isinstance(data, dict):
                return jsonify({
                    "ok": False,
                    "message": "Debes enviar un objeto JSON"
                }), 400

            try:
                id_pretriage = int(data.get("id_pretriage"))
            except (TypeError, ValueError):
                return jsonify({
                    "ok": False,
                    "message": "El id_pretriage no es válido"
                }), 400

            # Verificar autorización del paciente
            validar_acceso_pretriage(id_pretriage)
            # Verificar reglas y etapa de síntomas
            validar_evaluacion_inicial(
                id_pretriage,
                requerir_sintomas=True
            )

            # Generar o recuperar la pregunta pendiente
            resultado = self.service.generate_additional_questions(
                id_pretriage=id_pretriage
            )

            return jsonify({
                "ok": True,
                "id_pretriage": id_pretriage,
                "resultado": resultado
            }), 200

        except PermissionError as e:
            return jsonify({
                "ok": False,
                "message": str(e)
            }), 403

        except ValueError as e:
            return jsonify({
                "ok": False,
                "message": str(e)
            }), 400

        except Exception:
            import traceback
            traceback.print_exc()

            return jsonify({
                "ok": False,
                "message": "No fue posible generar la pregunta"
            }), 500


    # =========================================================
    # 3. GUARDAR RESPUESTA DEL PACIENTE
    # =========================================================

    @jwt_required()
    def guardar_respuesta(self):

        try:
            data = request.get_json(silent=True)

            if not isinstance(data, dict):
                return jsonify({
                    "ok": False,
                    "message": "Debes enviar un objeto JSON"
                }), 400

            try:
                id_pretriage = int(data.get("id_pretriage"))
                id_pregunta = int(data.get("id_pregunta"))
            except (TypeError, ValueError):
                return jsonify({
                    "ok": False,
                    "message": "Los IDs deben ser números válidos"
                }), 400

            respuesta = data.get("respuesta")

            # Verificar autorización y obtener el usuario
            id_user = validar_acceso_pretriage(id_pretriage)
            # Verificar que el pretriage pueda continuar
            validar_evaluacion_inicial(
                id_pretriage,
                requerir_sintomas=True
            )

            # Guardar la respuesta en PostgreSQL
            resultado = guardar_respuesta_ia(
                id_pretriage=id_pretriage,
                id_pregunta=id_pregunta,
                respuesta=respuesta,
                id_user=id_user
            )
            # Revisar el estado de seguridad después de guardar
            revision = revisar_seguridad_ia(
                id_pretriage=id_pretriage,
                id_user=id_user
            )
            db.session.commit()

            return jsonify({
                "ok": True,
                "resultado": resultado,
                "revision_seguridad": revision
            }), 200

        except PermissionError as e:
            db.session.rollback()
            return jsonify({
                "ok": False,
                "message": str(e)
            }), 403

        except ValueError as e:
            db.session.rollback()
            return jsonify({
                "ok": False,
                "message": str(e)
            }), 400

        except Exception:
            db.session.rollback()
            return jsonify({
                "ok": False,
                "message": "No fue posible guardar la respuesta"
            }), 500


    @jwt_required()
    def guardar_respuestas(self):

        try:

            data = request.get_json(silent=True)

            if not isinstance(data, dict):
                return jsonify({
                    "ok": False,
                    "message": "Debes enviar un objeto JSON"
                }), 400

            try:
                id_pretriage = int(
                    data.get("id_pretriage")
                )
            except (TypeError, ValueError):

                return jsonify({
                    "ok": False,
                    "message": "El id_pretriage no es válido"
                }), 400

            respuestas = data.get("respuestas")

            id_user = validar_acceso_pretriage(
                id_pretriage
            )

            validar_evaluacion_inicial(
                id_pretriage,
                requerir_sintomas=True
            )

            resultado = guardar_respuestas_ia(
                id_pretriage=id_pretriage,
                respuestas=respuestas,
                id_user=id_user
            )

            # UNA sola revisión para todo el bloque.
            revision = revisar_seguridad_ia(
                id_pretriage=id_pretriage,
                id_user=id_user
            )

            db.session.commit()

            return jsonify({
                "ok": True,
                "resultado": resultado,
                "revision_seguridad": revision
            }), 200

        except PermissionError as e:

            db.session.rollback()

            return jsonify({
                "ok": False,
                "message": str(e)
            }), 403

        except ValueError as e:

            db.session.rollback()

            return jsonify({
                "ok": False,
                "message": str(e)
            }), 400

        except Exception:

            db.session.rollback()

            return jsonify({
                "ok": False,
                "message": "No fue posible guardar las respuestas"
            }), 500

    @jwt_required()
    def clasificar_tipo_atencion(self):
        try:
            data = request.get_json(silent=True)

            if not isinstance(data, dict):
                return jsonify({
                    "ok": False,
                    "message": "Debes enviar un objeto JSON"
                }), 400

            try:
                id_pretriage = int(data.get("id_pretriage"))
            except (TypeError, ValueError):
                return jsonify({
                    "ok": False,
                    "message": "El id_pretriage no es válido"
                }), 400

            validar_acceso_pretriage(id_pretriage)

            resultado = self.service.classify_emergency_attention(
                id_pretriage
            )

            return jsonify({
                "ok": True,
                "id_pretriage": id_pretriage,
                **resultado
            }), 200

        except PermissionError as e:
            return jsonify({
                "ok": False,
                "message": str(e)
            }), 403

        except ValueError as e:
            return jsonify({
                "ok": False,
                "message": str(e)
            }), 400

        except Exception:
            return jsonify({
                "ok": False,
                "message": "No fue posible determinar el tipo de urgencia"
            }), 500
