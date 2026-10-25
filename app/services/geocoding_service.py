import json
import time

from functools import lru_cache
from threading import Lock
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


_rate_limit_lock = Lock()
_last_request_time = 0.0
MUNICIPIOS_PERMITIDOS = {
    "Medellín",
    "Envigado",
    "Bello",
    "Itagüí",
    "Sabaneta",
    "La Estrella",
    "Caldas",
}


@lru_cache(maxsize=512)
def _buscar_nominatim(query):
    global _last_request_time

    with _rate_limit_lock:
        elapsed = time.monotonic() - _last_request_time

        if elapsed < 1:
            time.sleep(1 - elapsed)

        params = {
            "q": query,
            "format": "jsonv2",
            "limit": 1,
            "countrycodes": "co",
            "addressdetails": 1,
        }

        url = (
            "https://nominatim.openstreetmap.org/search?"
            + urlencode(params)
        )

        req = Request(
            url,
            headers={
                "User-Agent": (
                    "Urgentia/1.0 "
                    "(https://github.com/dashanino/projectUrgentia)"
                ),
                "Accept-Language": "es",
            },
        )

        _last_request_time = time.monotonic()

        try:
            with urlopen(req, timeout=10) as response:
                data = json.load(response)

        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            raise RuntimeError(
                "El servicio de geocodificación no está disponible"
            ) from exc

        except (json.JSONDecodeError, ValueError) as exc:
            raise RuntimeError(
                "La respuesta de geocodificación no es válida"
            ) from exc

    if not data:
        return None

    result = data[0]

    try:
        return {
            "latitude": float(result["lat"]),
            "longitude": float(result["lon"]),
            "display_name": result.get("display_name", ""),
        }
    except (KeyError, TypeError, ValueError) as exc:
        raise RuntimeError(
            "No fue posible interpretar las coordenadas"
        ) from exc


def geocodificar_direccion(municipio, direccion):
    municipio = municipio.strip()
    direccion = direccion.strip()

    if not municipio or not direccion:
        raise ValueError(
            "Debes ingresar municipio y dirección"
        )
    if municipio not in MUNICIPIOS_PERMITIDOS:
        raise ValueError(
            "El municipio no está disponible para la búsqueda"
        )

    query = f"{direccion}, {municipio}, Colombia"

    return _buscar_nominatim(query)