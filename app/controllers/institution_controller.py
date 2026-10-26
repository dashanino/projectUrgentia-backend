from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.institution_service import (
    instituciones_cercanas_service,
    instituciones_por_servicio_cercanas_service,
    instituciones_valoracion_clinica_service
)
@jwt_required()
def instituciones_cercanas_controller():
    try:
        latitude = request.args.get("latitude", type=float)
        longitude = request.args.get("longitude", type=float)
        prioridad = request.args.get("prioridad")
        tipo_atencion = request.args.get("tipo_atencion")

        if latitude is None or longitude is None:
            return jsonify({
                "ok": False,
                "error": "Se requieren latitude y longitude"
            }), 400

        if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
            return jsonify({
                "ok": False,
                "error": "Las coordenadas no son válidas"
            }), 400

        if prioridad not in [
            "alta", "media_alta", "media_baja", "revision_clinica"
        ]:
            return jsonify({
                "ok": False,
                "error": "Prioridad no válida"
            }), 400
        
                # REVISIÓN CLÍNICA
        if prioridad == "revision_clinica":

            eps_id = request.args.get("eps_id", type=int)

            if eps_id is None or eps_id <= 0:
                return jsonify({
                    "ok": False,
                    "error": "Se requiere una EPS válida"
                }), 400

            instituciones = instituciones_valoracion_clinica_service(
                latitude=latitude,
                longitude=longitude,
                eps_id=eps_id,
                limite=3
            )

            return jsonify({
                "ok": True,
                "prioridad": "revision_clinica",
                "institutions": instituciones
            }), 200

        # PRIORIDAD MEDIA BAJA: SERVICIO RECOMENDADO
        if prioridad == "media_baja":

            servicio_recomendado = request.args.get(
                "servicio_recomendado"
            )

            eps_id = request.args.get("eps_id", type=int)

            if not servicio_recomendado:
                return jsonify({
                    "ok": False,
                    "error": "Se requiere servicio_recomendado"
                }), 400

            if eps_id is not None and eps_id <= 0:
                return jsonify({
                    "ok": False,
                    "error": "La EPS enviada no es válida"
                }), 400

            instituciones = instituciones_por_servicio_cercanas_service(
                latitude=latitude,
                longitude=longitude,
                servicio_recomendado=servicio_recomendado,
                eps_id=eps_id,
                limite=3
            )

            return jsonify({
                "ok": True,
                "prioridad": "media_baja",
                "servicio_recomendado": servicio_recomendado,
                "institutions": instituciones
            }), 200

        if prioridad not in ["alta", "media_alta"]:
            return jsonify({
                "ok": False,
                "error": "Prioridad no válida para búsqueda de instituciones"
            }), 400

        tipo_atencion = request.args.get("tipo_atencion")

        if not tipo_atencion:
            return jsonify({
                "ok": False,
                "error": "Se requiere tipo_atencion"
            }), 400

        instituciones = instituciones_cercanas_service(
            latitude=latitude,
            longitude=longitude,
            prioridad=prioridad,
            tipo_atencion=tipo_atencion,
            limite=3
        )

        return jsonify({
            "ok": True,
            "prioridad": prioridad,
            "tipo_atencion": tipo_atencion,
            "institutions": instituciones
        }), 200
    
    except ValueError as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 400


    except Exception:
        # Registra el error completo en el servidor con tu logger.
        return jsonify({
            "ok": False,
            "error": "No fue posible obtener las instituciones cercanas"
        }), 500