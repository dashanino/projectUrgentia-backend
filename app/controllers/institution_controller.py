from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.institution_service import instituciones_cercanas_service

@jwt_required()
def instituciones_cercanas_controller():

    try:

        latitude = request.args.get("latitude", type=float)
        longitude = request.args.get("longitude", type=float)
        prioridad = request.args.get("prioridad")

        # -----------------------------------------------------
        # Validaciones
        # -----------------------------------------------------

        if latitude is None or longitude is None:
            return jsonify({
                "ok": False,
                "error": "Se requieren latitude y longitude"
            }), 400

        if prioridad not in [
            "alta",
            "media_alta",
            "media_baja"
        ]:
            return jsonify({
                "ok": False,
                "error": "Prioridad no válida"
            }), 400

        # -----------------------------------------------------
        # Buscar instituciones
        # -----------------------------------------------------

        instituciones = instituciones_cercanas_service(
            latitude=latitude,
            longitude=longitude,
            prioridad=prioridad
        )

        return jsonify({
            "ok": True,
            "prioridad": prioridad,
            "institutions": instituciones
        }), 200

    except Exception as e:

        return jsonify({
            "ok": False,
            "error": "No fue posible obtener las instituciones cercanas",
            "detalle": str(e)
        }), 500