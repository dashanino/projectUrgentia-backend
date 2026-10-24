from types import SimpleNamespace
from unittest.mock import patch

import pytest
from flask import Flask

from app.services.clinical_access_service import (
    validar_acceso_clinico,
)


@pytest.fixture
def app():
    return Flask(__name__)


def usuario(role="doctor", activo=True, rol_activo=True):
    return SimpleNamespace(
        id=10,
        is_active=activo,
        role=SimpleNamespace(
            name=role,
            is_active=rol_activo,
        ),
    )


def ejecutar_validacion(app, user, claims=None):
    with app.app_context():
        with (
            patch(
                "app.services.clinical_access_service.get_jwt",
                return_value=claims or {},
            ),
            patch(
                "app.services.clinical_access_service.get_jwt_identity",
                return_value="10",
            ),
            patch(
                "app.services.clinical_access_service.db.session.get",
                return_value=user,
            ),
        ):
            return validar_acceso_clinico()


def test_doctor_activo_autorizado(app):
    doctor = usuario()

    resultado = ejecutar_validacion(app, doctor)

    assert resultado is doctor


@pytest.mark.parametrize(
    "rol",
    ["patient", "usernn", "admin"],
)
def test_otros_roles_rechazados(app, rol):
    with pytest.raises(PermissionError):
        ejecutar_validacion(app, usuario(role=rol))


def test_doctor_inactivo_rechazado(app):
    with pytest.raises(PermissionError):
        ejecutar_validacion(app, usuario(activo=False))


def test_rol_inactivo_rechazado(app):
    with pytest.raises(PermissionError):
        ejecutar_validacion(app, usuario(rol_activo=False))


def test_usuario_inexistente_rechazado(app):
    with pytest.raises(PermissionError):
        ejecutar_validacion(app, None)


def test_token_emergencia_rechazado(app):
    with pytest.raises(PermissionError):
        ejecutar_validacion(
            app,
            usuario(),
            claims={"tipo_acceso": "emergencia"},
        )