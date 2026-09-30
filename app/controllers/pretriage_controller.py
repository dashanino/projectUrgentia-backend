import traceback
from flask import jsonify, request
from flask_jwt_extended import (get_jwt, get_jwt_identity,jwt_required)
from app.extensions import db
from app.models.pretriage import Pretriage
from app.services.pretriage_service import iniciar_pretriage_nn
from app.services.pretriage_antecedente_service import guardar_antecedentes_nn
from app.services.pretriage_service import guardar_poblacion_nn
from app.services.red_flag_service import obtener_banderas_rojas
from app.services.pretriage_red_flag_service import guardar_banderas_rojas_nn


def iniciar_pretriage_nn_controller():
    try:
        # 1. Crear el usuario NN, su pretriaje y generar el token
        resultado = iniciar_pretriage_nn()

        # 2. Devolver la respuesta
        return jsonify({
            "message": "Pretriaje iniciado correctamente",
            "id_user": resultado["id_user"],
            "id_pretriage": resultado["id_pretriage"],
            "access_token": resultado["access_token"]
        }), 201

    except ValueError as e:
        # Error de validación
        return jsonify({
            "error": str(e)
        }), 400

    except Exception:
        # Mostrar el error completo en la terminal
        traceback.print_exc()

        # Devolver una respuesta genérica a Postman
        return jsonify({
            "error": "No se pudo iniciar el pretriaje"
        }), 500
def guardar_antecedentes_nn_controller(id_pretriage):
    try:
        # 1. Obtener los antecedentes enviados
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "error": "Debes enviar un JSON válido"
            }), 400

        if "id_antecedentes" not in data:
            return jsonify({
                "error": "Falta el campo id_antecedentes"
            }), 400

        # 2. Obtener los datos del token JWT
        id_user_token = get_jwt_identity()
        claims = get_jwt()

        # 3. Verificar que sea un acceso de emergencias
        if claims.get("tipo_acceso") != "emergencia":
            return jsonify({
                "error": "El token no corresponde a un acceso de emergencias"
            }), 403

        # 4. Verificar que el token corresponda al pretriaje
        if claims.get("id_pretriage") != id_pretriage:
            return jsonify({
                "error": "No tienes permiso para modificar este pretriaje"
            }), 403

        # 5. Verificar que el usuario sea el propietario
        pretriage = db.session.get(Pretriage, id_pretriage)

        if pretriage is None:
            return jsonify({
                "error": "El pretriaje no existe"
            }), 404

        if str(pretriage.id_user) != str(id_user_token):
            return jsonify({
                "error": "No tienes permiso para modificar este pretriaje"
            }), 403

        # 6. Guardar los antecedentes
        resultado = guardar_antecedentes_nn(
            id_pretriage=id_pretriage,
            ids_antecedentes=data["id_antecedentes"]
        )

        # 7. Devolver la respuesta
        return jsonify({
            "message": "Antecedentes guardados correctamente",
            **resultado
        }), 200

    except ValueError as e:
        return jsonify({
            "error": str(e)
        }), 400

    except Exception:
        traceback.print_exc()

        return jsonify({
            "error": "No se pudieron guardar los antecedentes"
        }), 500
@jwt_required()
def guardar_poblacion_nn_controller(id_pretriage):

    try:
        # 1. Obtener los datos del token
        claims = get_jwt()
        id_user = int(get_jwt_identity())

        # 2. Validar que sea un acceso de emergencias
        if claims.get("tipo_acceso") != "emergencia":
            return jsonify({
                "error": "El token no corresponde a un acceso de emergencias"
            }), 403

        # 3. Comprobar que el token corresponde al pretriaje
        if claims.get("id_pretriage") != id_pretriage:
            return jsonify({
                "error": "No tienes permiso para modificar este pretriaje"
            }), 403

        # 4. Obtener la población enviada
        datos = request.get_json(silent=True)

        if not isinstance(datos, dict):
            return jsonify({
                "error": "Debes enviar un objeto JSON"
            }), 400

        id_poblacion = datos.get("id_poblacion")

        if type(id_poblacion) is not int:
            return jsonify({
                "error": "El ID de población debe ser un número entero"
            }), 400

        # 5. Guardar la población
        resultado = guardar_poblacion_nn(
            id_pretriage,
            id_user,
            id_poblacion
        )

        return jsonify({
            "message": "Población guardada correctamente",
            **resultado
        }), 200

    except PermissionError as e:
        return jsonify({
            "error": str(e)
        }), 403

    except ValueError as e:
        return jsonify({
            "error": str(e)
        }), 400

    except Exception:
        traceback.print_exc()

        return jsonify({
            "error": "No se pudo guardar la población"
        }), 500
@jwt_required()
def obtener_banderas_rojas_controller(id_pretriage):

    try:
        # 1. Obtener los datos del token JWT
        claims = get_jwt()
        id_user = int(get_jwt_identity())

        # 2. Verificar que sea un acceso de emergencias
        if claims.get("tipo_acceso") != "emergencia":
            return jsonify({
                "error": "El token no corresponde a un acceso de emergencias"
            }), 403

        # 3. Verificar que el token corresponda al pretriaje
        if claims.get("id_pretriage") != id_pretriage:
            return jsonify({
                "error": "No tienes permiso para consultar este pretriaje"
            }), 403

        # 4. Consultar las banderas rojas
        resultado = obtener_banderas_rojas(
            id_pretriage,
            id_user
        )

        # 5. Devolver la respuesta
        return jsonify(resultado), 200

    except PermissionError as e:
        return jsonify({
            "error": str(e)
        }), 403

    except ValueError as e:
        return jsonify({
            "error": str(e)
        }), 400

    except Exception:
        traceback.print_exc()

        return jsonify({
            "error": "No se pudieron consultar las banderas rojas"
        }), 500
@jwt_required()
def guardar_banderas_rojas_nn_controller(id_pretriage):

    try:
        # 1. Obtener datos del token
        claims = get_jwt()
        id_user = int(get_jwt_identity())

        # 2. Verificar acceso de emergencia
        if claims.get("tipo_acceso") != "emergencia":
            return jsonify({
                "error": "El token no corresponde a un acceso de emergencias"
            }), 403

        # 3. Verificar que el token corresponde al pretriaje
        if claims.get("id_pretriage") != id_pretriage:
            return jsonify({
                "error": "No tienes permiso para modificar este pretriaje"
            }), 403

        # 4. Obtener JSON
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "error": "Debes enviar un objeto JSON"
            }), 400

        if "id_banderas" not in data:
            return jsonify({
                "error": "Falta el campo id_banderas"
            }), 400

        # 5. Guardar banderas seleccionadas
        resultado = guardar_banderas_rojas_nn(
            id_pretriage=id_pretriage,
            id_user=id_user,
            ids_banderas=data["id_banderas"]
        )

        return jsonify({
            "message": "Banderas rojas guardadas correctamente",
            **resultado
        }), 200

    except PermissionError as e:
        return jsonify({
            "error": str(e)
        }), 403

    except ValueError as e:
        return jsonify({
            "error": str(e)
        }), 400

    except Exception:
        traceback.print_exc()

        return jsonify({
            "error": "No se pudieron guardar las banderas rojas"
        }), 500