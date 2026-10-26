import json
import re
import time
import unicodedata
from functools import lru_cache
from threading import Lock
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

_rate_limit_lock = Lock()
_last_request_time = 0.0

MUNICIPIOS_PERMITIDOS = {
    "Medellín", "Envigado", "Bello", "Itagüí", "Sabaneta", "La Estrella", "Caldas"
}

_VIA_RE = re.compile(
    r"\b(carrera|cra\.?|cr\.?|calle|cl\.?|avenida|av\.?|"
    r"transversal|transv\.?|tv\.?|diagonal|diag\.?)\s*"
    r"([0-9]{1,3}\s*[a-z]?(?:\s*(?:sur|norte|este|oeste))?)\b",
    re.IGNORECASE,
)
_NUMERO_CASA_RE = re.compile(
    r"(?:#\s*|\bno\.?\s*|\bnumero\s*)?"
    r"([0-9]{1,4}\s*[a-z]?\s*[-–]\s*[0-9]{1,4}\s*[a-z]?)",
    re.IGNORECASE,
)
_ALIAS_VIA = {
    "carrera": "carrera", "cra": "carrera", "cr": "carrera",
    "calle": "calle", "cl": "calle",
    "avenida": "avenida", "av": "avenida",
    "transversal": "transversal", "transv": "transversal", "tv": "transversal",
    "diagonal": "diagonal", "diag": "diagonal",
}
_VIA_TYPES = {
    "road", "street", "residential", "unclassified", "tertiary", "secondary",
    "primary", "service", "living_street", "pedestrian", "tertiary_link",
    "secondary_link", "primary_link", "trunk", "trunk_link", "highway",
    "roadway", "minor_road", "living_street", "track",
}


def _norm(value):
    if not isinstance(value, str):
        return ""
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", value).strip().lower()


def _normalizar_numero(value):
    return re.sub(r"[^a-z0-9]", "", _norm(value))


def _clave_via(value):
    match = _VIA_RE.search(value or "")
    if not match:
        return None
    tipo = _norm(match.group(1)).replace(".", "")
    tipo = _ALIAS_VIA.get(tipo)
    numero = re.sub(r"\s+", "", _norm(match.group(2)))
    if not tipo or not numero:
        return None
    return f"{tipo} {numero}"


def _extraer_direccion(direccion):
    via = _VIA_RE.search(direccion or "")
    if not via:
        raise ValueError("Escribe una vía válida, por ejemplo: Carrera 43A #32-39.")
    numero = _NUMERO_CASA_RE.search(direccion, via.end())
    if not numero:
        raise ValueError("Incluye el número de la dirección, por ejemplo: Carrera 43A #32-39.")
    return via.group(0).strip(), _clave_via(via.group(0)), numero.group(1).strip()


def _municipio_coincide(candidato, municipio):
    address = candidato.get("address") or {}
    esperado = _norm(municipio)
    # Usar los campos que describen municipio/ciudad; no confundir barrio o comuna con municipio.
    for key in ("city", "town", "municipality", "village"):
        value = _norm(address.get(key, ""))
        if value:
            if value == esperado:
                return True
    # Algunas respuestas omiten city pero incluyen la localidad en display_name.
    partes = [_norm(part) for part in (candidato.get("display_name") or "").split(",")]
    return esperado in partes


def _pais_y_departamento_coinciden(candidato):
    address = candidato.get("address") or {}
    country_code = _norm(address.get("country_code", ""))
    country = _norm(address.get("country", ""))
    if country_code:
        if country_code != "co":
            return False
    elif country and country not in {"colombia", "republica de colombia"}:
        return False

    state = _norm(address.get("state", ""))
    if state and state not in {"antioquia", "departamento de antioquia"}:
        return False
    if not state:
        partes = [_norm(part) for part in (candidato.get("display_name") or "").split(",")]
        if "antioquia" not in partes:
            return False
    return True

def _via_candidato(candidato):
    address = candidato.get("address") or {}
    sources = [
        address.get("road", ""),
        candidato.get("name", ""),
        (candidato.get("display_name") or "").split(",")[0],
    ]
    for source in sources:
        key = _clave_via(source)
        if key:
            return key
    return None


def _base_coincide(candidato, municipio, via_esperada):
    if not _pais_y_departamento_coinciden(candidato):
        return False
    if not _municipio_coincide(candidato, municipio):
        return False
    return _via_candidato(candidato) == via_esperada


def _numero_coincide(candidato, numero_esperado):
    address = candidato.get("address") or {}
    numero = _normalizar_numero(address.get("house_number", ""))
    return bool(numero and numero == _normalizar_numero(numero_esperado))


@lru_cache(maxsize=512)
def _buscar_nominatim_cached(params_tuple):
    global _last_request_time
    params = dict(params_tuple)
    with _rate_limit_lock:
        elapsed = time.monotonic() - _last_request_time
        if elapsed < 1.0:
            time.sleep(1.0 - elapsed)
        url = "https://nominatim.openstreetmap.org/search?" + urlencode(params)
        request = Request(
            url,
            headers={
                "User-Agent": "Urgentia/1.0 (https://github.com/dashanino/projectUrgentia)",
                "Accept-Language": "es",
            },
        )
        _last_request_time = time.monotonic()
        try:
            with urlopen(request, timeout=12) as response:
                data = json.load(response)
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            raise RuntimeError("El servicio de geocodificación no está disponible") from exc
        except (json.JSONDecodeError, ValueError) as exc:
            raise RuntimeError("La respuesta de geocodificación no es válida") from exc
    if not isinstance(data, list):
        raise RuntimeError("La respuesta de geocodificación tiene un formato inesperado")
    return data
def _buscar_nominatim(params):
    return _buscar_nominatim_cached(tuple(sorted((str(k), str(v)) for k, v in params.items())))


def _coordenadas(candidato):
    try:
        lat = float(candidato["lat"])
        lon = float(candidato["lon"])
    except (KeyError, TypeError, ValueError) as exc:
        raise RuntimeError("No fue posible interpretar las coordenadas de la dirección") from exc
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        raise RuntimeError("El servicio devolvió coordenadas no válidas")
    return lat, lon


def _params_busqueda(street, municipio, structured=True):
    common = {
        "format": "jsonv2",
        "limit": "10",
        "addressdetails": "1",
        "countrycodes": "co",
    }
    if structured:
        common.update({
            "street": street,
            "city": municipio,
            "state": "Antioquia",
            "country": "Colombia",
        })
    else:
        common["q"] = f"{street}, {municipio}, Antioquia, Colombia"
    return common


def _es_resultado_via(candidato):
    address = candidato.get("address") or {}
    if address.get("house_number"):
        # No usar otra vivienda numerada como sustituto de la dirección solicitada.
        return False
    addresstype = _norm(candidato.get("addresstype", ""))
    osm_type = _norm(candidato.get("type", ""))
    osm_class = _norm(candidato.get("class", candidato.get("category", "")))
    return addresstype in _VIA_TYPES or osm_type in _VIA_TYPES or osm_class in {"highway", "road"}


def geocodificar_direccion(municipio, direccion):
    """Devuelve coordenadas exactas o un punto de vía claramente marcado como aproximado."""
    municipio_input = _norm(municipio)
    municipio_canonico = next(
        (item for item in MUNICIPIOS_PERMITIDOS if _norm(item) == municipio_input),
        None,
    )
    if not municipio_canonico:
        raise ValueError("El municipio no está disponible para la búsqueda")
    if not isinstance(direccion, str) or not direccion.strip():
        raise ValueError("Debes ingresar municipio y dirección")

    via_texto, via_esperada, numero_texto = _extraer_direccion(direccion.strip())

    # 1. Búsqueda estructurada de la dirección completa. Se evita que el motor trate
    # el número como parte del nombre de la vía dentro de una consulta libre.
    candidatos_exactos = _buscar_nominatim(
        _params_busqueda(f"{via_texto} {numero_texto}", municipio_canonico, structured=True)
    )
    exactos = [
        c for c in candidatos_exactos
        if _base_coincide(c, municipio_canonico, via_esperada)
        and _numero_coincide(c, numero_texto)
    ]
    if exactos:
        exactos.sort(key=lambda c: -float(c.get("importance") or 0))
        elegido = exactos[0]
        lat, lon = _coordenadas(elegido)
        return {
            "latitude": lat,
            "longitude": lon,
            "display_name": elegido.get("display_name", ""),
            "is_approximate": False,
            "precision_message": "Se encontró una coincidencia con la vía, el municipio y el número de dirección.",
        }

    # 2. Fallback: buscar la vía sin número. Se permite solo un objeto de vía,
    # del mismo municipio y departamento, con nombre de vía coincidente.
    candidatos_via = _buscar_nominatim(
        _params_busqueda(via_texto, municipio_canonico, structured=True)
    )
    vias = [
        c for c in candidatos_via
        if _base_coincide(c, municipio_canonico, via_esperada) and _es_resultado_via(c)
    ]

    # 3. Segunda variante de consulta para los datos cartográficos que no responden
    # bien al formato estructurado. Se mantiene la misma validación antes de aceptar.
    if not vias:
        candidatos_via = _buscar_nominatim(
            _params_busqueda(via_texto, municipio_canonico, structured=False)
        )
        vias = [
            c for c in candidatos_via
            if _base_coincide(c, municipio_canonico, via_esperada) and _es_resultado_via(c)
        ]

    if not vias:
        return None

    vias.sort(key=lambda c: -float(c.get("importance") or 0))
    elegido = vias[0]
    lat, lon = _coordenadas(elegido)
    return {
        "latitude": lat,
        "longitude": lon,
        "display_name": elegido.get("display_name", ""),
        "is_approximate": True,
        "precision_message": (
            "No se encontró el número exacto. Este punto corresponde a la vía en el municipio indicado, "
            "no necesariamente al inmueble. Las distancias serán aproximadas; confirma antes de continuar."
        ),
    }

    
