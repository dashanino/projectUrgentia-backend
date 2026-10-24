from types import SimpleNamespace

from app.services import pretriage_service as servicio


def test_creacion_pretriage_nn(mocker):
    rol = SimpleNamespace(id=2, name="usernn")

    consulta = mocker.MagicMock()
    consulta.scalar_one_or_none.return_value = rol

    mocker.patch.object(
        servicio.db.session,
        "execute",
        return_value=consulta,
    )

    objetos = []

    def simular_add(objeto):
        objetos.append(objeto)

    def simular_flush():
        if len(objetos) >= 1:
            objetos[0].id = 101
        if len(objetos) >= 2:
            objetos[1].id = 202

    mocker.patch.object(
        servicio.db.session,
        "add",
        side_effect=simular_add,
    )

    mocker.patch.object(
        servicio.db.session,
        "flush",
        side_effect=simular_flush,
    )

    commit = mocker.patch.object(
        servicio.db.session,
        "commit",
    )

    token = mocker.patch.object(
        servicio,
        "create_access_token",
        return_value="token_simulado",
    )

    resultado = servicio.iniciar_pretriage_nn()

    assert resultado["id_user"] == 101
    assert resultado["id_pretriage"] == 202
    assert resultado["access_token"] == "token_simulado"

    assert objetos[1].id_user == 101
    assert objetos[1].estado == "iniciado"

    commit.assert_called_once()

    token.assert_called_once_with(
        identity="101",
        additional_claims={
            "id_pretriage": 202,
            "tipo_acceso": "emergencia",
        },
    )
