from flask import jsonify, request

from app.services.role_service import create_role, get_all_roles


def create_role_controller():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Falta llenar los campos del request"}), 400

    name = data.get("name")
    description = data.get("description")

    if not name:
        return jsonify({"error": "El campo name es obligatorio"}), 400

    try:
        role = create_role(name=name, description=description)
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

    return jsonify(role_to_dict(role)), 201


def get_all_roles_controller():
    roles = get_all_roles()
    return jsonify([role_to_dict(r) for r in roles]), 200


def role_to_dict(role):
    return {
        "id": role.id,
        "name": role.name,
        "description": role.description,
    }