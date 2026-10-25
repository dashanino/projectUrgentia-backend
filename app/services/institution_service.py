from math import radians, sin, cos, sqrt, atan2

from app.models.institution import Institution
from app.models.emergency_attention import EmergencyAttention
from app.models.institution_emergency_attention import (
    InstitutionEmergencyAttention
)


# Niveles de complejidad institucional permitidos por prioridad.
# Debes validar esta correspondencia con tu protocolo clínico.
NIVELES_POR_PRIORIDAD = {
    "alta": [3, 4],
    "media_alta": [3, 4],
    "media_baja": [2, 3],
}

# Deben coincidir EXACTAMENTE con emergency_attentions.name
TIPOS_ATENCION = {
    "general": "Urgencias Generales",
    "pediatrica": "Urgencias Pediátricas",
    "ginecoobstetrica": "Urgencias Ginecoobstétricas",
    "trauma": "Urgencias de Trauma",
    "neurologica": "Urgencias Neurológicas",
    "cardiovascular": "Urgencias Cardiovasculares",
}


def instituciones_cercanas_service(
    latitude,
    longitude,
    prioridad,
    tipo_atencion,
    limite=3
):
    niveles = NIVELES_POR_PRIORIDAD.get(prioridad)
    nombre_atencion = TIPOS_ATENCION.get(tipo_atencion)

    if not niveles or not nombre_atencion:
        return []

    atencion = EmergencyAttention.query.filter_by(
        name=nombre_atencion,
        is_active=True
    ).first()

    if not atencion:
        return []

    # Primero se seleccionan únicamente las instituciones con
    # la categoría de urgencia correspondiente.
    instituciones = (
        Institution.query
        .join(
            InstitutionEmergencyAttention,
            InstitutionEmergencyAttention.institution_id
            == Institution.id
        )
        .filter(
            InstitutionEmergencyAttention.emergency_attention_id
            == atencion.id,
            InstitutionEmergencyAttention.is_active.is_(True),
            Institution.is_active.is_(True),
            Institution.latitude.isnot(None),
            Institution.longitude.isnot(None),
            Institution.level.in_(niveles)
        )
        .distinct()
        .all()
    )

    resultados = []

    for institution in instituciones:
        distancia = calcular_distancia_km(
            latitude,
            longitude,
            float(institution.latitude),
            float(institution.longitude)
        )

        resultados.append({
            "id": institution.id,
            "name": institution.name,
            "type": institution.type,
            "level": institution.level,
            "municipality": institution.municipality,
            "address": institution.address,
            "latitude": float(institution.latitude),
            "longitude": float(institution.longitude),
            "distance_km": round(distancia, 2),
        })

    resultados.sort(key=lambda item: item["distance_km"])
    return resultados[:limite]


def calcular_distancia_km(lat1, lon1, lat2, lon2):
    radio_tierra = 6371.0

    lat1, lon1, lat2, lon2 = map(
        radians, [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return radio_tierra * c