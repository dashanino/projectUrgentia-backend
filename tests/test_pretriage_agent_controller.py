from unittest.mock import patch

from flask import Flask

from app.controllers.pretriage_agent_controller import (
    PretriageAgentController,
)


def crear_cliente():
    app = Flask(__name__)
    app.config["TESTING"] = True
    return app.test_client(), app


def registrar_ruta(app, controlador):
    app.add_url_rule(
        "/test/respuesta",
        view_func=lambda: controlador.guardar_respuesta.__wrapped__(
            controlador
        ),
        methods=["POST"],
    )


def test_respuesta_confirma_transaccion(mocker):
    controlador = object.__new__(PretriageAgentController)
    cliente, app = crear_cliente()
    registrar_ruta(app, controlador)

    mocker.patch(
        "app.controllers.pretriage_agent_controller.validar_acceso_pretriage",
        return_value=10,
    )
    mocker.patch(
        "app.controllers.pretriage_agent_controller.validar_evaluacion_inicial"
    )
    mocker.patch(
        "app.controllers.pretriage_agent_controller.guardar_respuesta_ia",
        return_value={"respuesta_guardada": True},
    )
    mocker.patch(
        "app.controllers.pretriage_agent_controller.revisar_seguridad_ia",
        return_value={"accion": "revision_clinica"},
    )

    commit = mocker.patch(
        "app.controllers.pretriage_agent_controller.db.session.commit"
    )

    respuesta = cliente.post(
        "/test/respuesta",
        json={
            "id_pretriage": 1,
            "id_pregunta": 2,
            "respuesta": "Respuesta simulada",
        },
    )

    assert respuesta.status_code == 200
    assert respuesta.json["ok"] is True
    commit.assert_called_once()


def test_error_revision_revierte_transaccion(mocker):
    controlador = object.__new__(PretriageAgentController)
    cliente, app = crear_cliente()
    registrar_ruta(app, controlador)

    mocker.patch(
        "app.controllers.pretriage_agent_controller.validar_acceso_pretriage",
        return_value=10,
    )
    mocker.patch(
        "app.controllers.pretriage_agent_controller.validar_evaluacion_inicial"
    )
    mocker.patch(
        "app.controllers.pretriage_agent_controller.guardar_respuesta_ia",
        return_value={"respuesta_guardada": True},
    )
    mocker.patch(
        "app.controllers.pretriage_agent_controller.revisar_seguridad_ia",
        side_effect=RuntimeError("Fallo simulado"),
    )

    commit = mocker.patch(
        "app.controllers.pretriage_agent_controller.db.session.commit"
    )
    rollback = mocker.patch(
        "app.controllers.pretriage_agent_controller.db.session.rollback"
    )

    respuesta = cliente.post(
        "/test/respuesta",
        json={
            "id_pretriage": 1,
            "id_pregunta": 2,
            "respuesta": "Respuesta simulada",
        },
    )

    assert respuesta.status_code == 500
    assert respuesta.json["ok"] is False
    commit.assert_not_called()
    rollback.assert_called_once()
