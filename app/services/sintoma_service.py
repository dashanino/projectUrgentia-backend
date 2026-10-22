from app.models.sintoma import Sintoma

def sintoma_redflag_service(id_bandera):
    sintomas = (
        Sintoma.query
        .filter_by(id_bandera=id_bandera)
        .order_by(Sintoma.id)
        .all()
    )

    return [
    {
        'id': sintoma.id,
        'nombre': sintoma.name,
        'id_bandera': sintoma.id_bandera
    }
    for sintoma in sintomas
]