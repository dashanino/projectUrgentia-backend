
from flask import jsonify
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models.pretriage_red_flag import PretriageRedFlag
from app.models.sintoma import Sintoma

from app.services.triage_rule_service import evaluar_reglas_triage
from app.services.pretriage_access_service import validar_acceso_pretriage


@jwt_required()
def evaluar_reglas_triage_controller(id_pretriage):

    try:
        # 1. Validar acceso del paciente
        id_user = validar_acceso_pretriage(id_pretriage)

        # 2. Evaluar reglas de alta prioridad
        resultado_reglas = evaluar_reglas_triage(
            id_pretriage=id_pretriage,
            id_user=id_user
        )

        # 3. Si se activa una regla de alta prioridad,
        # devolver la alerta inmediatamente.
        if resultado_reglas["alta_prioridad"] is True:

            return jsonify({
                "ok": True,
                "id_pretriage": id_pretriage,
                "origen": "reglas",
                "alta_prioridad": True,
                "accion": "alerta",
                "resultado": resultado_reglas
            }), 200

        # 4. Consultar las banderas seleccionadas
        banderas = (
            db.session.query(PretriageRedFlag.id_bandera)
            .filter(
                PretriageRedFlag.id_pretriage == id_pretriage
            )
            .all()
        )

        ids_banderas = [
            fila.id_bandera
            for fila in banderas
        ]

        # 5. Si no hay banderas, continuar con IA
        if not ids_banderas:

            return jsonify({
                "ok": True,
                "id_pretriage": id_pretriage,
                "origen": "reglas",
                "alta_prioridad": False,
                "accion": "continuar_ia"
            }), 200

        # 6. Comprobar si las banderas tienen síntomas
        sintomas = (
            db.session.query(Sintoma.id)
            .filter(
                Sintoma.id_bandera.in_(ids_banderas)
            )
            .first()
        )

        # 7. Si existen síntomas asociados,
        # mostrar primero esa sección.
        if sintomas is not None:

            return jsonify({
                "ok": True,
                "id_pretriage": id_pretriage,
                "origen": "reglas",
                "alta_prioridad": False,
                "accion": "continuar_submenu"
            }), 200

        # 8. Si no existen síntomas asociados,
        # continuar directamente con IA.
        return jsonify({
            "ok": True,
            "id_pretriage": id_pretriage,
            "origen": "reglas",
            "alta_prioridad": False,
            "accion": "continuar_ia"
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
            "error": "Ocurrió un error al evaluar las reglas de triage"
        }), 500
