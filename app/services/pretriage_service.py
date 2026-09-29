from sqlalchemy import select
from flask_jwt_extended import create_access_token

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
        db.session.flush()

        # 3. Crear el pretriaje asociado
        pretriage = Pretriage(
            id_user=user_nn.id,
            estado="iniciado"
        )

        db.session.add(pretriage)
        db.session.flush()

        # 4. Obtener los identificadores
        id_user = user_nn.id
        id_pretriage = pretriage.id

        # 5. Confirmar los registros
        db.session.commit()

        # 6. Generar el token JWT
        access_token = create_access_token(
            identity=str(id_user),
            additional_claims={
                "id_pretriage": id_pretriage,
                "tipo_acceso": "emergencia"
            }
        )

        return {
            "id_user": id_user,
            "id_pretriage": id_pretriage,
            "access_token": access_token
        }

    except Exception:
        db.session.rollback()
        raise