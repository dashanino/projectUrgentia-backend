from sqlalchemy import select

from app.extensions import db
from app.models.user import User
from app.models.role import Role
from app.models.pretriage import Pretriage


def iniciar_pretriage_nn():

    try:
        # 1. Buscar el rol usernn
        rol_usernn = db.session.execute(
            select(Role).where(Role.name == "usernn")
        ).scalar_one_or_none()

        if rol_usernn is None:
            raise ValueError("El rol usernn no existe")

        # 2. Crear el usuario NN
        user_nn = User(
            id_role=rol_usernn.id
        )

        db.session.add(user_nn)

        # Obtener el ID sin confirmar la transacción
        db.session.flush()

        # 3. Crear el pretriaje asociado
        pretriage = Pretriage(
            id_user=user_nn.id,
            estado="iniciado"
        )

        db.session.add(pretriage)

        # 4. Guardar ambos registros
        db.session.commit()

        return user_nn, pretriage

    except Exception:
        db.session.rollback()
        raise