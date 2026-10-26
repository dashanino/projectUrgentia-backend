from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.services.geocoding_service import geocodificar_direccion

location_bp = Blueprint("location", __name__)


@location_bp.route("/location/geocode", methods=["GET"])
@jwt_required()
def geocode_location():
    municipio = request.args.get("municipio", "").strip()
    consulta = request.args.get("direccion", "").strip()

    if not municipio or not consulta:
        return jsonify({
            "ok": False,
            "error": "Indica el municipio y una dirección o nombre de lugar.",
        }), 400

    if len(municipio) > 120 or len(consulta) > 250:
        return jsonify({
            "ok": False,
            "error": "El municipio o la búsqueda son demasiado largos.",
        }), 400

    try:
        candidatos = geocodificar_direccion(municipio, consulta)
        if not candidatos:
            # La consulta se procesó correctamente; cero coincidencias no es
            # un fallo de la ruta. Devolver 200 evita un error HTTP rojo y deja
            # que Angular presente el mensaje útil dentro del formulario.
            return jsonify({
                "ok": True,
                "query": consulta,
                "municipio": municipio,
                "candidates": [],
                "error": (
                    "No encontramos coincidencias para esa búsqueda. "
                    "Prueba con el nombre oficial completo, agrega una dirección "
                    "o utiliza el GPS."
                ),
            }), 200

        # La API devuelve candidatos y NO fija automáticamente coordenadas en el primer
        # resultado. Angular debe mostrar la lista y pedir al usuario que elija uno.
        return jsonify({
            "ok": True,
            "query": consulta,
            "municipio": municipio,
            "candidates": candidatos,
        }), 200

    except ValueError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400
    except RuntimeError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 502
    except Exception:
        # No se exponen trazas internas al cliente.
        return jsonify({
            "ok": False,
            "error": "No fue posible buscar la ubicación. Inténtalo nuevamente.",
        }), 500
