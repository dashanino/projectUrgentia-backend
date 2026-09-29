from flask import jsonify
from app.services.pretriage_service import iniciar_pretriage_nn


def iniciar_pretriage_nn_controller():
    try:
        user_nn, pretriage = iniciar_pretriage_nn()

        return jsonify({
            "message": "Pretriaje iniciado correctamente",
            "id_user": user_nn.id,
            "id_pretriage": pretriage.id
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception:
        return jsonify({
            "error": "No se pudo iniciar el pretriaje"
        }), 500