from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.institution_service import instituciones_cercanas_service

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
            "alta", "media_alta", "media_baja"
        ]:
            return jsonify({
                "ok": False,
                "error": "Prioridad no válida"
            }), 400

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

    except Exception:
        # Registra el error completo en el servidor con tu logger.
        return jsonify({
            "ok": False,
            "error": "No fue posible obtener las instituciones cercanas"
        }), 500