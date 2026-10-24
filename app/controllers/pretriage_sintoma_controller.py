
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from app.services.pretriage_sintoma_service import guardar_sintomas_pretriage


@jwt_required()
def guardar_sintomas_pretriage_controller(id_pretriage):

    try:
        id_user = int(get_jwt_identity())
        claims = get_jwt()

        # Verificar acceso de emergencia
        if claims.get("tipo_acceso") != "emergencia":
            return jsonify({
                "ok": False,
                "error": "Este endpoint requiere acceso de emergencia"
            }), 403

        # Verificar que el token pertenezca al pretriage
        try:
            id_pretriage_token = int(claims.get("id_pretriage"))
        except (TypeError, ValueError):
            return jsonify({
                "ok": False,
                "error": "El token no contiene un pretriage válido"
            }), 403

        if id_pretriage_token != id_pretriage:
            return jsonify({
                "ok": False,
                "error": "No tienes permiso para modificar este pretriage"
            }), 403

        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "ok": False,
                "error": "Debes enviar un objeto JSON"
            }), 400

        ids_sintomas = data.get("ids_sintomas")

        resultado = guardar_sintomas_pretriage(
            id_pretriage=id_pretriage,
            id_user=id_user,
            ids_sintomas=ids_sintomas
        )

        return jsonify({
            "ok": True,
            "accion": "iniciar_ia",
            "resultado": resultado
        }), 200

    except PermissionError as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 403

    except ValueError as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 400

    except Exception:
        return jsonify({
            "ok": False,
            "error": "No fue posible guardar los síntomas"
        }), 500
