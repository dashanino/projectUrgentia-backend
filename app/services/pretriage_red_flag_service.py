
from app.extensions import db
from app.models.pretriage_sintoma import PretriageSintoma
from app.models.pretriage import Pretriage
from app.models.red_flag import RedFlag
from app.models.poblacion_red_flag import PoblacionRedFlag
from app.models.pretriage_red_flag import PretriageRedFlag

from app.services.pretriage_evaluation_service import (
    invalidar_evaluacion_reglas
)


def guardar_banderas_rojas_nn(
    id_pretriage,
    id_user,
    ids_banderas
):

    # 1. Buscar el pretriage
    pretriage = db.session.get(
        Pretriage,
        id_pretriage
    )

    if pretriage is None:
        raise ValueError("El pretriage no existe")

    # 2. Verificar que pertenezca al usuario
    if pretriage.id_user != id_user:
        raise PermissionError(
            "No tienes permiso para modificar este pretriage"
        )

    # 3. Verificar que siga iniciado
    if pretriage.estado != "iniciado":
        raise ValueError(
            "El pretriage ya no se encuentra iniciado"
        )

    # 4. Verificar que tenga población
    if pretriage.id_poblacion is None:
        raise ValueError(
            "Primero debes seleccionar una población"
        )

    # 5. Validar la lista
    if not isinstance(ids_banderas, list):
        raise ValueError(
            "id_banderas debe ser una lista"
        )

    if any(
        type(id_bandera) is not int
        for id_bandera in ids_banderas
    ):
        raise ValueError(
            "Todos los IDs de las banderas deben ser enteros"
        )

    # Evitar IDs repetidos
    ids_banderas = list(set(ids_banderas))

    # 6. Buscar banderas permitidas
    asociaciones = (
        db.session.query(PoblacionRedFlag)
        .join(
            RedFlag,
            RedFlag.id == PoblacionRedFlag.id_bandera
        )
        .filter(
            PoblacionRedFlag.id_poblacion == pretriage.id_poblacion,
            RedFlag.is_active.is_(True)
        )
        .all()
    )

    ids_permitidos = {
        asociacion.id_bandera
        for asociacion in asociaciones
    }

    # 7. Validar que correspondan a la población
    ids_invalidos = [
        id_bandera
        for id_bandera in ids_banderas
        if id_bandera not in ids_permitidos
    ]

    if ids_invalidos:
        raise ValueError(
            f"Las banderas {ids_invalidos} no pertenecen "
            "a la población seleccionada"
        )

    try:
        # 8. Invalidar evaluación anterior
        invalidar_evaluacion_reglas(pretriage)

        # 9. Eliminar síntomas anteriores
        db.session.query(PretriageSintoma).filter(
            PretriageSintoma.id_pretriage == id_pretriage
        ).delete(synchronize_session=False)

        # 10. Reiniciar la etapa de síntomas
        pretriage.sintomas_completados = False

        # 11. Eliminar banderas anteriores
        db.session.query(PretriageRedFlag).filter(
            PretriageRedFlag.id_pretriage == id_pretriage
        ).delete(synchronize_session=False)

        # 12. Guardar nuevas banderas
        for id_bandera in ids_banderas:
            seleccion = PretriageRedFlag(
                id_pretriage=id_pretriage,
                id_bandera=id_bandera
            )

            db.session.add(seleccion)

        # 13. Confirmar todos los cambios
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise