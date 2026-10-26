from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.services.geocoding_service import geocodificar_direccion

location_bp = Blueprint("location", __name__)


@location_bp.route("/location/geocode", methods=["GET"])
@jwt_required()
def geocode_location():
    municipio = request.args.get("municipio", "").strip()
    direccion = request.args.get("direccion", "").strip()

    if not municipio or not direccion:
        return jsonify({"ok": False, "error": "Debes ingresar municipio y dirección"}), 400
    if len(municipio) > 120 or len(direccion) > 250:
        return jsonify({"ok": False, "error": "El municipio o la dirección son demasiado largos"}), 400

    try:
        resultado = geocodificar_direccion(municipio=municipio, direccion=direccion)
        if resultado is None:
            return jsonify({
                "ok": False,
                "error": (
                    "No encontramos la vía en el municipio indicado. "
                    "Verifica los datos o utiliza tu ubicación GPS."
                ),
            }), 404
        return jsonify({"ok": True, **resultado}), 200
    except ValueError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400
    except RuntimeError as exc:
        return jsonify({
            "ok": False,
            "error": (
                "No fue posible consultar el servicio de mapas. "
                "Inténtalo de nuevo o utiliza tu ubicación GPS."
            ),
        }), 502
