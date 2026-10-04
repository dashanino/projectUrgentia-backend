from flask import jsonify
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from app.services.triage_rule_service import evaluar_reglas_triaje


@jwt_required()
def evaluar_reglas_triaje_controller(id_pretriage):
    try:
        # Obtener usuario y datos del token
        id_user = int(get_jwt_identity())
        claims = get_jwt()

        # Verificar que sea acceso de emergencia
        if claims.get("tipo_acceso") != "emergencia":
            return jsonify({
                "error": "Este endpoint requiere acceso de emergencia"
            }), 403

        # Verificar que el pretriaje del token
        # sea el mismo que se quiere evaluar
        id_pretriage_token = claims.get("id_pretriage")

        if id_pretriage_token != id_pretriage:
            return jsonify({
                "error": "No tienes permiso para evaluar este pretriaje"
            }), 403

        # Evaluar las reglas
        resultado = evaluar_reglas_triaje(
            id_pretriage=id_pretriage,
            id_user=id_user
        )

        return jsonify(resultado), 200

    except PermissionError as e:
        return jsonify({
            "error": str(e)
        }), 403

    except ValueError as e:
        return jsonify({
            "error": str(e)
        }), 400

    except Exception as e:
        return jsonify({
            "error": "Ocurrió un error al evaluar las reglas de triaje",
            "detalle": str(e)
        }), 500