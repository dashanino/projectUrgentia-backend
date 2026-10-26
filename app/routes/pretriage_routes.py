from flask import Blueprint, jsonify
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from sqlalchemy import select
from datetime import date
from app.models.poblacion import Poblacion
from app.extensions import db
from app.models.user import User
from app.models.patient import Patient
from app.models.pretriage import Pretriage
from app.models.patient_antecedente import PatientAntecedente
from app.models.pretriage_antecedente import PretriageAntecedente
from flask import request
from app.services.pretriage_access_service import validar_acceso_pretriage
from app.services.pretriage_service import guardar_poblacion_nn
from app.controllers.pretriage_controller import (
    iniciar_pretriage_nn_controller,
    guardar_antecedentes_nn_controller,
    guardar_poblacion_nn_controller,
    obtener_banderas_rojas_controller,
    guardar_banderas_rojas_nn_controller,
)

from app.controllers.triage_rule_controller import (
    evaluar_reglas_triage_controller
)

pretriage_bp = Blueprint("pretriage", __name__)


# Iniciar el acceso de emergencias
@pretriage_bp.route("/pretriage", methods=["POST"])
def emergency_access():
    return iniciar_pretriage_nn_controller()
@pretriage_bp.route("/pretriage/registrado", methods=["POST"])
@jwt_required()
def iniciar_pretriage_registrado():

    claims = get_jwt()

    if claims.get("tipo_acceso") is not None:
        return jsonify({
            "error": "Esta opción requiere una cuenta registrada"
        }), 403

    try:
        id_user = int(get_jwt_identity())
    except (ValueError, TypeError):
        return jsonify({"error": "Token inválido"}), 401

    user = db.session.get(User, id_user)

    if user is None or not user.is_active:
        return jsonify({
            "error": "Usuario no encontrado o inactivo"
        }), 404

    patient = db.session.execute(
        select(Patient).where(Patient.user_id == id_user)
    ).scalar_one_or_none()

    if patient is None:
        return jsonify({
            "error": "El usuario no tiene un perfil de paciente"
        }), 404

    # 1. Calcular la edad desde PostgreSQL
    if patient.birth_date is None:
        return jsonify({
            "error": "Debes registrar tu fecha de nacimiento antes de iniciar"
        }), 400

    hoy = date.today()
    nacimiento = patient.birth_date

    if nacimiento > hoy:
        return jsonify({
            "error": "La fecha de nacimiento no es válida"
        }), 400

    edad = (
        hoy.year - nacimiento.year
        - ((hoy.month, hoy.day) < (nacimiento.month, nacimiento.day))
    )

    # 2. Determinar población general por edad
    if edad < 18:
        nombre_poblacion = "Niño"
    elif edad >= 60:
        nombre_poblacion = "Adulto Mayor"
    else:
        nombre_poblacion = "Adulto"

    poblacion = db.session.execute(
        select(Poblacion).where(
            Poblacion.name == nombre_poblacion,
            Poblacion.is_active.is_(True)
        )
    ).scalar_one_or_none()

    if poblacion is None:
        return jsonify({
            "error": "No se encontró una población activa para el paciente"
        }), 400

    try:
        # 3. Crear evaluación con población automática
        pretriage = Pretriage(
            id_user=id_user,
            id_eps=patient.id_eps,
            id_poblacion=poblacion.id,
            estado="iniciado"
        )

        db.session.add(pretriage)
        db.session.flush()

        # 4. Recuperar antecedentes del paciente
        antecedentes_paciente = db.session.execute(
            select(PatientAntecedente).where(
                PatientAntecedente.id_paciente == patient.id
            )
        ).scalars().all()

        ids_antecedentes = {
            antecedente.id_antecedente
            for antecedente in antecedentes_paciente
        }

        # 5. Copiar antecedentes al pre-triage
        for id_antecedente in ids_antecedentes:
            db.session.add(
                PretriageAntecedente(
                    id_pretriage=pretriage.id,
                    id_antecedente=id_antecedente
                )
            )

        # Solo marcar completa esta etapa cuando existan
        # antecedentes registrados. Si no hay ninguno,
        # requeriremos confirmar que no tiene antecedentes.
        pretriage.antecedentes_completados = bool(ids_antecedentes)

        db.session.commit()

        return jsonify({
            "message": "Evaluación iniciada correctamente",
            "id_pretriage": pretriage.id,
            "id_poblacion": poblacion.id,
            "poblacion": poblacion.name,
            "edad": edad,
            "antecedentes_precargados": len(ids_antecedentes),
            "antecedentes_completados": pretriage.antecedentes_completados,
            "requiere_confirmacion_antecedentes": not bool(ids_antecedentes),
            "requiere_confirmacion_poblacion_especial": True
        }), 201

    except Exception:
        db.session.rollback()
        return jsonify({
            "error": "No se pudo iniciar la evaluación"
        }), 500


# Guardar los antecedentes del usuario NN
@pretriage_bp.route(
    "/pretriage/<int:id_pretriage>/antecedentes",
    methods=["POST"]
)
@jwt_required()
def save_emergency_antecedents(id_pretriage):
    return guardar_antecedentes_nn_controller(id_pretriage)
@pretriage_bp.route(
    "/pretriage/<int:id_pretriage>/poblacion",
    methods=["POST"]
)
@jwt_required()
def guardar_poblacion(id_pretriage):
    return guardar_poblacion_nn_controller(id_pretriage)
# Consultar banderas rojas
@pretriage_bp.route(
    "/pretriage/<int:id_pretriage>/banderas-rojas",
    methods=["GET"]
)
@jwt_required()
def consultar_banderas_rojas(id_pretriage):
    return obtener_banderas_rojas_controller(id_pretriage)


# Guardar banderas rojas
@pretriage_bp.route(
    "/pretriage/<int:id_pretriage>/banderas-rojas",
    methods=["POST"]
)
@jwt_required()
def guardar_banderas_rojas(id_pretriage):
    return guardar_banderas_rojas_nn_controller(id_pretriage)

@pretriage_bp.route(
    "/pretriage/<int:id_pretriage>/evaluar-triage",
    methods=["POST"]
)
def evaluar_triage(id_pretriage):
    return evaluar_reglas_triage_controller(id_pretriage)
@pretriage_bp.route(
    "/pretriage/<int:id_pretriage>/confirmacion-clinica",
    methods=["POST"]
)
@jwt_required()
def confirmar_clinica_registrado(id_pretriage):

    # Este endpoint es exclusivo para pacientes registrados.
    if get_jwt().get("tipo_acceso") is not None:
        return jsonify({
            "error": "Esta opción requiere una cuenta registrada"
        }), 403

    try:
        id_user = validar_acceso_pretriage(id_pretriage)

        datos = request.get_json(silent=True)

        if not isinstance(datos, dict):
            return jsonify({
                "error": "Debes enviar las respuestas de confirmación"
            }), 400

        accidente = datos.get("accidente")
        embarazo = datos.get("embarazo")
        antecedentes_actualizados = datos.get("antecedentes_actualizados")

        if (
            type(accidente) is not bool
            or type(antecedentes_actualizados) is not bool
            or embarazo not in (True, False, None)
        ):
            return jsonify({
                "error": "Las respuestas enviadas no son válidas"
            }), 400

        if not antecedentes_actualizados:
            return jsonify({
                "error": "Debes actualizar tu información médica antes de continuar"
            }), 400

        # Una evaluación con embarazo y trauma simultáneos
        # necesita una ruta que considere ambas condiciones.
        if accidente and embarazo is True:
            return jsonify({
                "error": (
                    "Se reportaron embarazo y trauma simultáneamente. "
                    "Esta combinación requiere valoración médica prioritaria "
                    "y no puede continuar por la ruta automática actual."
                )
            }), 409

        pretriage = db.session.get(Pretriage, id_pretriage)

        # No confiar en la población recibida desde Angular.
        # Recuperamos la población general desde la fecha de nacimiento.
        patient = db.session.execute(
            select(Patient).where(Patient.user_id == id_user)
        ).scalar_one_or_none()

        if patient is None or patient.birth_date is None:
            return jsonify({
                "error": "No se encontró una fecha de nacimiento válida"
            }), 400

        from datetime import date

        hoy = date.today()
        nacimiento = patient.birth_date

        if nacimiento > hoy:
            return jsonify({
                "error": "La fecha de nacimiento no es válida"
            }), 400

        edad = (
            hoy.year - nacimiento.year
            - ((hoy.month, hoy.day) < (nacimiento.month, nacimiento.day))
        )

        if edad < 18:
            poblacion_general = "Niño"
        elif edad >= 60:
            poblacion_general = "Adulto Mayor"
        else:
            poblacion_general = "Adulto"

        # Las condiciones especiales prevalecen sobre la
        # población general cuando se presentan individualmente.
        if accidente:
            nombre_poblacion = "Trauma/Accidente"
        elif embarazo is True:
            nombre_poblacion = "Embarazada"
        else:
            nombre_poblacion = poblacion_general

        poblacion = db.session.execute(
            select(Poblacion).where(
                Poblacion.name == nombre_poblacion,
                Poblacion.is_active.is_(True)
            )
        ).scalar_one_or_none()

        if poblacion is None:
            return jsonify({
                "error": "La población requerida no está disponible"
            }), 400

        resultado = guardar_poblacion_nn(
            id_pretriage,
            id_user,
            poblacion.id
        )

        return jsonify({
            "ok": True,
            "message": "Población clínica actualizada",
            "id_pretriage": resultado["id_pretriage"],
            "id_poblacion": resultado["id_poblacion"],
            "poblacion": resultado["poblacion"],
            "antecedentes_actualizados": True
        }), 200

    except PermissionError as error:
        return jsonify({"error": str(error)}), 403

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except Exception:
        db.session.rollback()
        return jsonify({
            "error": "No se pudo confirmar la información clínica"
        }), 500