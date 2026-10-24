from math import radians, sin, cos, sqrt, atan2

from app.extensions import db
from app.models.institution import Institution


def instituciones_cercanas_service(
    latitude,
    longitude,
    prioridad,
    limite=3
):
    """
    Busca instituciones activas cercanas al usuario,
    filtrando según la prioridad del pretriaje.
    """

    # ---------------------------------------------------------
    # 1. Determinar nivel de complejidad requerido
    # ---------------------------------------------------------

    niveles_por_prioridad = {
        "alta": [3, 4],
        "media_alta": [3],
        "media_baja": [2, 3],
    }

    niveles_permitidos = niveles_por_prioridad.get(prioridad)

    if not niveles_permitidos:
        return []

    # ---------------------------------------------------------
    # 2. Buscar instituciones activas con ubicación
    # ---------------------------------------------------------

    instituciones = (
        Institution.query
        .filter(
            Institution.is_active.is_(True),
            Institution.latitude.isnot(None),
            Institution.longitude.isnot(None),
            Institution.level.in_(niveles_permitidos)
        )
        .all()
    )

    # ---------------------------------------------------------
    # 3. Calcular distancia
    # ---------------------------------------------------------

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
            "distance_km": round(distancia, 2)
        })

    # ---------------------------------------------------------
    # 4. Ordenar de más cercana a más lejana
    # ---------------------------------------------------------

    resultados.sort(key=lambda x: x["distance_km"])

    # ---------------------------------------------------------
    # 5. Devolver máximo 3
    # ---------------------------------------------------------

    return resultados[:limite]


def calcular_distancia_km(
    lat1,
    lon1,
    lat2,
    lon2
):
    """
    Calcula la distancia entre dos coordenadas
    usando la fórmula de Haversine.
    """

    R = 6371.0  # radio de la Tierra en km

    lat1 = radians(lat1)
    lon1 = radians(lon1)

    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c