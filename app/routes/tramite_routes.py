
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

from app.models.tramite import Tramite
from app.models.eps_tramite import EPSTramite


@tramite_bp.route("/eps/<int:eps_id>/tramites/<string:codigo>", methods=["GET"])
def obtener_tramite_eps(eps_id, codigo):

    eps = EPS.query.filter_by(
        id=eps_id,
        is_active=True
    ).first()

    if not eps:
        return jsonify({
            "error": "EPS no encontrada"
        }), 404

    tramite = Tramite.query.filter_by(
        code=codigo,
        is_active=True
    ).first()

    if not tramite:
        return jsonify({
            "error": "Trámite no encontrado"
        }), 404

    informacion = EPSTramite.query.filter_by(
        eps_id=eps.id,
        tramite_id=tramite.id,
        is_active=True
    ).first()

    if not informacion:
        return jsonify({
            "eps": eps.name,
            "tramite": tramite.name,
            "disponible": False,
            "mensaje": "La orientación específica para este trámite aún no está disponible."
        }), 200

    return jsonify({
        "eps": eps.name,
        "tramite": tramite.name,
        "disponible": True,
        "requisitos": informacion.requisitos or [],
        "pasos": informacion.pasos or [],
        "url_oficial": informacion.url_oficial,
        "fecha_verificacion": (
            informacion.fecha_verificacion.isoformat()
            if informacion.fecha_verificacion
            else None
        )
    }), 200