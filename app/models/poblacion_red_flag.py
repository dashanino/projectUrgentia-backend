from app.extensions import db


class PoblacionRedFlag(db.Model):
    __tablename__ = "poblacion_red_flags"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    id_poblacion = db.Column(
        db.Integer,
        db.ForeignKey("poblaciones.id"),
        nullable=False
    )

    id_bandera = db.Column(
        db.Integer,
        db.ForeignKey("red_flags.id"),
        nullable=False
    )

    # Relaciones
    poblacion = db.relationship(
        "Poblacion",
        back_populates="banderas_asociadas"
    )

    red_flag = db.relationship(
        "RedFlag",
        back_populates="poblaciones_asociadas"
    )

    # Evitar asociar dos veces la misma bandera
    # con la misma población
    __table_args__ = (
        db.UniqueConstraint(
            "id_poblacion",
            "id_bandera",
            name="uq_poblacion_red_flag"
        ),
    )