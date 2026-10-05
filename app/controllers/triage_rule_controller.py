from flask import jsonify
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from app.services.triage_rule_service import evaluar_reglas_triage
from app.services.pretriage_agent_service import PretriageAgentService


@jwt_required()
def evaluar_reglas_triage_controller(id_pretriage):

    try:
        # =========================================================
        # 1. OBTENER USUARIO Y DATOS DEL TOKEN
        # =========================================================

        id_user = int(get_jwt_identity())
        claims = get_jwt()

        # =========================================================
        # 2. VERIFICAR QUE SEA ACCESO DE EMERGENCIA
        # =========================================================

        if claims.get("tipo_acceso") != "emergencia":
            return jsonify({
                "error": "Este endpoint requiere acceso de emergencia"
            }), 403

        # =========================================================
        # 3. VERIFICAR QUE EL PRETRIAGE DEL TOKEN
        #    SEA EL MISMO QUE SE QUIERE EVALUAR
        # =========================================================

        id_pretriage_token = claims.get("id_pretriage")

        if id_pretriage_token is None:
            return jsonify({
                "error": "El token no contiene un id_pretriage"
            }), 403

        try:
            id_pretriage_token = int(id_pretriage_token)

        except (TypeError, ValueError):
            return jsonify({
                "error": "El id_pretriage del token no es válido"
            }), 403

        if id_pretriage_token != id_pretriage:
            return jsonify({
                "error": "No tienes permiso para evaluar este pretriage"
            }), 403

        # =========================================================
        # 4. EVALUAR PRIMERO LAS REGLAS DE TRIAGE
        # =========================================================

        resultado_reglas = evaluar_reglas_triage(
            id_pretriage=id_pretriage,
            id_user=id_user
        )

        # =========================================================
        # 5. SI UNA REGLA DETERMINA ALTA PRIORIDAD
        #    TERMINAR EL FLUJO AQUÍ
        # =========================================================

        if resultado_reglas.get("alta_prioridad") is True:

            return jsonify({
                "ok": True,
                "id_pretriage": id_pretriage,
                "origen": "reglas",
                "alta_prioridad": True,
                "accion": "alerta",
                "resultado": resultado_reglas
            }), 200

        # =========================================================
        # 6. SI NO HAY ALTA PRIORIDAD POR REGLAS,
        #    CONTINUAR CON LA IA
        # =========================================================

        agente = PretriageAgentService()

        resultado_ia = agente.evaluate(
            id_pretriage=id_pretriage
        )

        # =========================================================
        # 7. DEVOLVER EL RESULTADO DE LA IA
        # =========================================================

        return jsonify({
            "ok": True,
            "id_pretriage": id_pretriage,
            "origen": "ia",
            "alta_prioridad": resultado_ia.get("prioridad") == "alta",
            "accion": "resultado_ia",
            "resultado": resultado_ia
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

    except Exception as e:

        return jsonify({
            "ok": False,
            "error": "Ocurrió un error al evaluar el triage",
            "detalle": str(e)
        }), 500