
from flask import Blueprint, jsonify
from app.models.eps import EPS

tramite_bp = Blueprint(
    "tramites",
    __name__,
    url_prefix="/api/tramites"
)


@tramite_bp.route("/health", methods=["GET"])
def tramites_health():
    return jsonify({
        "message": "Módulo de trámites funcionando correctamente"
    }), 200


@tramite_bp.route("/eps", methods=["GET"])
def obtener_eps():
    eps_activas = (
        EPS.query
        .filter_by(is_active=True)
        .order_by(EPS.name)
        .all()
    )

    resultado = [
        {
            "id": eps.id,
            "nombre": eps.name
        }
        for eps in eps_activas
    ]

    return jsonify(resultado), 200

