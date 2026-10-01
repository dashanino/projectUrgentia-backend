from flask import jsonify, request

from app.services.poblacion_service import create_poblacion, get_all_poblaciones


def create_poblacion_controller():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Falta llenar los campos del request"}), 400

    name = data.get("name")
    description = data.get("description")

    if not name:
        return jsonify({"error": "El campo name es obligatorio"}), 400

    try:
        role = create_poblacion(name=name, description=description)
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

    return jsonify(role_to_dict(role)), 201


def get_all_poblaciones_controller():
    poblaciones = get_all_poblaciones()
    return jsonify([role_to_dict(p) for p in poblaciones]), 200


def role_to_dict(poblacion):
    return {
        "id": poblacion.id,
        "name": poblacion.name,
        "description": poblacion.description,
    }