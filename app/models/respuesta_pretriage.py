from datetime import datetime, timezone
from app.extensions import db


class RespuestaPretriage(db.Model):
    __tablename__ = "respuestas_pretriage"

    id = db.Column(db.Integer, primary_key=True)

    id_pretriage = db.Column(
        db.Integer,
        db.ForeignKey("pretriages.id"),
        nullable=False
    )

    id_submenu = db.Column(
        db.Integer,
        db.ForeignKey("submenu_red_flags.id"),
        nullable=False
    )

    respuesta = db.Column(db.Text, nullable=False)
    

    fecha_creacion = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    pretriage = db.relationship("Pretriage", back_populates="respuestas")
    submenu = db.relationship("SubmenuRedFlag", back_populates="respuestas")

    __table_args__ = (
        db.UniqueConstraint("id_pretriage", "id_submenu", name="uq_pretriage_submenu"),
    )