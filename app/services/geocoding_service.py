"""Búsqueda explícita de direcciones y lugares para Urgentia usando Nominatim.

Acepta direcciones, edificios, apartamentos, clínicas, hospitales, universidades,
comercios y otros lugares indexados por OpenStreetMap. Devuelve candidatos para
que el usuario elija uno; no selecciona automáticamente el primer resultado.
"""

from functools import lru_cache
from threading import Lock
from time import monotonic, sleep
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
import re
import unicodedata


_RATE_LIMIT_LOCK = Lock()
_LAST_REQUEST_TIME = 0.0

MUNICIPIOS_PERMITIDOS = {
    "Medellín", "Envigado", "Bello", "Itagüí", "Sabaneta", "La Estrella", "Caldas"
}

_VIA_RE = re.compile(
    r"\b(carrera|cra\.?|cr\.?|calle|cl\.?|avenida|av\.?|"
    r"transversal|transv\.?|tv\.?|diagonal|diag\.?)\s*"
    r"([0-9]{1,3}\s*[a-z]?(?:\s*(?:sur|norte|este|oeste))?)\b",
    re.IGNORECASE,
)
_CASA_RE = re.compile(
    r"(?:#\s*|\bno\.?\s*|\bnumero\s*)?"
    r"([0-9]{1,4}\s*[a-z]?\s*[-–]\s*[0-9]{1,4}\s*[a-z]?)",
    re.IGNORECASE,
)
_VIA_ALIAS = {
    "carrera": "carrera", "cra": "carrera", "cr": "carrera",
    "calle": "calle", "cl": "calle",
    "avenida": "avenida", "av": "avenida",
    "transversal": "transversal", "transv": "transversal", "tv": "transversal",
    "diagonal": "diagonal", "diag": "diagonal",
}
_VIA_TYPES = {
    "road", "street", "residential", "unclassified", "tertiary", "secondary",
    "primary", "service", "living_street", "pedestrian", "tertiary_link",
    "secondary_link", "primary_link", "trunk", "trunk_link", "track",
}
_TYPE_LABELS = {
    "hospital": "Hospital", "clinic": "Clínica", "doctors": "Consultorio médico",
    "pharmacy": "Farmacia", "university": "Universidad", "school": "Institución educativa",
    "apartments": "Edificio de apartamentos", "apartment": "Apartamento",
    "residential": "Urbanización o zona residencial", "housing": "Conjunto residencial",
    "residential_unit": "Unidad residencial", "residential_complex": "Conjunto residencial",
    "neighbourhood": "Barrio o sector", "neighborhood": "Barrio o sector",
    "quarter": "Barrio o sector", "suburb": "Sector urbano", "city_district": "Sector urbano",
    "apartments": "Edificio de apartamentos", "landuse": "Zona residencial o urbana",
    "house": "Dirección residencial", "commercial": "Edificio o zona comercial",
    "building": "Edificio", "hotel": "Hotel", "mall": "Centro comercial",
    "shopping_centre": "Centro comercial", "road": "Vía", "street": "Vía",
    "pedestrian": "Vía peatonal", "restaurant": "Restaurante",
    "supermarket": "Supermercado", "bank": "Banco", "parking": "Estacionamiento",
    "place_of_worship": "Lugar de culto", "landuse": "Zona residencial o urbana",
}


def _normalizar(texto):
    if not isinstance(texto, str):
        return ""
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(ch for ch in texto if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", texto).strip().lower()


def _canonizar_municipio(municipio):
    buscado = _normalizar(municipio)
    return next((m for m in MUNICIPIOS_PERMITIDOS if _normalizar(m) == buscado), None)


def _clave_via(texto):
    match = _VIA_RE.search(texto or "")
    if not match:
        return None
    tipo = _VIA_ALIAS.get(_normalizar(match.group(1)).replace(".", ""))
    numero = re.sub(r"\s+", "", _normalizar(match.group(2)))
    return f"{tipo} {numero}" if tipo and numero else None


def _consulta_es_direccion(consulta):
    via = _VIA_RE.search(consulta or "")
    if not via:
        return None
    casa = _CASA_RE.search(consulta, via.end())
    return {
        "via_texto": via.group(0).strip(),
        "via_clave": _clave_via(via.group(0)),
        "numero_texto": casa.group(1).strip() if casa else None,
    }


def _buscar_nominatim(params):
    """Busca solo al enviar el formulario; aplica límite de 1 req/s y caché."""
    frozen = tuple(sorted((str(k), str(v)) for k, v in params.items()))
    return _buscar_nominatim_cached(frozen)


@lru_cache(maxsize=512)
def _buscar_nominatim_cached(params_frozen):
    global _LAST_REQUEST_TIME
    params = dict(params_frozen)

    with _RATE_LIMIT_LOCK:
        elapsed = monotonic() - _LAST_REQUEST_TIME
        if elapsed < 1.0:
            sleep(1.0 - elapsed)

        url = "https://nominatim.openstreetmap.org/search?" + urlencode(params)
        request = Request(
            url,
            headers={
                "User-Agent": "Urgentia/1.0 (https://github.com/dashanino/projectUrgentia)",
                "Accept-Language": "es",
            },
        )
        _LAST_REQUEST_TIME = monotonic()

        try:
            with urlopen(request, timeout=12) as response:
                data = json.load(response)
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            raise RuntimeError("El servicio de mapas no está disponible temporalmente.") from exc
        except (json.JSONDecodeError, ValueError) as exc:
            raise RuntimeError("El servicio de mapas devolvió una respuesta no válida.") from exc

    if not isinstance(data, list):
        raise RuntimeError("La respuesta del servicio de mapas tiene un formato inesperado.")
    return data


def _parametros_texto_libre(consulta, municipio, variante=0):
    """Construye consultas de texto libre, de más específica a más amplia.

    No fija una capa temática: universidades, edificios y otros POI pueden
    estar etiquetados de formas distintas en OpenStreetMap.
    """
    consultas = [
        f"{consulta}, {municipio}, Antioquia, Colombia",
        f"{consulta}, {municipio}, Colombia",
        f"{consulta}, Antioquia, Colombia",
        consulta,
    ]
    variante = max(0, min(variante, len(consultas) - 1))
    return {
        "q": consultas[variante],
        "format": "jsonv2",
        "limit": "10",
        "addressdetails": "1",
        "namedetails": "1",
        "countrycodes": "co",
    }


def _parametros_via(via, municipio):
    return {
        "street": via,
        "city": municipio,
        "state": "Antioquia",
        "country": "Colombia",
        "format": "jsonv2",
        "limit": "8",
        "addressdetails": "1",
        "countrycodes": "co",
        "layer": "address",
    }


def _partes_display(candidato):
    return [_normalizar(parte) for parte in (candidato.get("display_name") or "").split(",")]


def _coincide_municipio_pais(candidato, municipio):
    """Valida la ubicación sin descartar todos los lugares residenciales.

    Nominatim no siempre rellena ``city`` en objetos que representan unidades,
    urbanizaciones o barrios. Se comprueban país/departamento, localidades
    administrativas y componentes completos de ``display_name``. Si existe
    una localidad principal que coincide con otro municipio permitido, se
    rechaza para no mover silenciosamente la búsqueda a otro municipio.
    """
    address = candidato.get("address") or {}
    codigo_pais = _normalizar(address.get("country_code", ""))
    pais = _normalizar(address.get("country", ""))

    if codigo_pais and codigo_pais != "co":
        return False
    if pais and pais not in {"colombia", "republica de colombia"}:
        return False

    departamento = _normalizar(address.get("state", ""))
    if departamento and "antioquia" not in departamento:
        return False

    target = _normalizar(municipio)
    municipios_permitidos_norm = {_normalizar(m) for m in MUNICIPIOS_PERMITIDOS}

    def coincide(valor):
        valor = _normalizar(valor)
        return bool(valor) and (
            valor == target
            or re.search(rf"\b{re.escape(target)}\b", valor) is not None
        )

    # La coincidencia en estos campos tiene la prioridad más alta.
    campos_localidad_principal = ("city", "town", "village")
    localidades_principales = [
        _normalizar(address.get(key, ""))
        for key in campos_localidad_principal
        if address.get(key)
    ]
    if any(coincide(valor) for valor in localidades_principales):
        return True

    # Si Nominatim declara otra localidad que es inequívocamente uno de los
    # municipios soportados por Urgentia, no aceptamos el candidato como si
    # perteneciera al municipio buscado.
    municipios_principales_conocidos = [
        valor for valor in localidades_principales
        if valor in municipios_permitidos_norm
    ]
    if municipios_principales_conocidos and target not in municipios_principales_conocidos:
        return False

    # Según cómo esté mapeada una urbanización, Medellín/Sabaneta/etc. puede
    # aparecer en otro campo administrativo o de localidad de OSM.
    campos_secundarios = (
        "municipality", "county", "state_district", "city_district",
        "suburb", "neighbourhood", "neighborhood", "quarter", "borough",
        "district",
    )
    if any(coincide(address.get(key, "")) for key in campos_secundarios):
        return True

    # display_name suele incluir todos los componentes de la jerarquía; exigir
    # un componente completo evita coincidencias accidentales de subcadenas.
    if target in _partes_display(candidato):
        return True

    return False


def _numero_normalizado(valor):
    return re.sub(r"[^a-z0-9]", "", _normalizar(str(valor or "")))


def _candidato_es_via(candidato):
    address = candidato.get("address") or {}
    tipo = _normalizar(candidato.get("type", ""))
    categoria = _normalizar(candidato.get("category", candidato.get("class", "")))
    addresstype = _normalizar(candidato.get("addresstype", ""))
    return (
        addresstype in _VIA_TYPES
        or tipo in _VIA_TYPES
        or categoria in {"highway", "road"}
        or bool(address.get("road")) and tipo in _VIA_TYPES
    )


def _clave_via_candidato(candidato):
    address = candidato.get("address") or {}
    for texto in (
        address.get("road", ""),
        candidato.get("name", ""),
        (candidato.get("display_name") or "").split(",")[0],
    ):
        clave = _clave_via(texto)
        if clave:
            return clave
    return None


def _etiqueta_tipo(candidato):
    tipo = _normalizar(candidato.get("type", ""))
    categoria = _normalizar(candidato.get("category", candidato.get("class", "")))
    address_type = _normalizar(candidato.get("addresstype", ""))
    for key in (tipo, categoria, address_type):
        if key in _TYPE_LABELS:
            return _TYPE_LABELS[key]
    return (tipo or address_type or "Lugar").replace("_", " ").capitalize()


def _nombre_candidato(candidato):
    name = candidato.get("name")
    if not name:
        namedetails = candidato.get("namedetails") or {}
        name = namedetails.get("name:es") or namedetails.get("name")
    if not name:
        name = (candidato.get("display_name") or "Ubicación encontrada").split(",")[0]
    return str(name).strip()


def _convertir_candidato(candidato, municipio, consulta, direccion):
    if not _coincide_municipio_pais(candidato, municipio):
        return None

    try:
        latitude = float(candidato["lat"])
        longitude = float(candidato["lon"])
    except (KeyError, TypeError, ValueError):
        return None
    if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
        return None

    address = candidato.get("address") or {}
    display_name = str(candidato.get("display_name") or "").strip()
    if not display_name:
        return None

    tipo = _normalizar(candidato.get("type", ""))
    categoria = _normalizar(candidato.get("category", candidato.get("class", "")))
    place_id = candidato.get("place_id")
    osm_type = candidato.get("osm_type") or "place"
    osm_id = candidato.get("osm_id") or place_id or f"{latitude}:{longitude}"
    candidate_id = f"{osm_type}:{osm_id}"

    location_kind = "named_place"
    is_approximate = False
    precision_message = (
        "Punto del lugar registrado en OpenStreetMap. Confirma que corresponde al edificio o establecimiento correcto; puede señalar su centro y no su entrada."
    )

    if direccion:
        entrada = direccion["numero_texto"]
        via_esperada = direccion["via_clave"]
        via_candidata = _clave_via_candidato(candidato)
        numero_candidato = address.get("house_number", "")

        # No aceptar otra vía ni un número de inmueble diferente.
        if via_candidata != via_esperada:
            return None

        if entrada:
            if numero_candidato:
                if _numero_normalizado(numero_candidato) != _numero_normalizado(entrada):
                    return None
                location_kind = "exact_address"
                precision_message = "El mapa registra una coincidencia con la vía y el número indicado. Comprueba que la dirección mostrada sea la correcta."
            else:
                # Si no se confirma el número, solo permitir el objeto que representa la vía.
                if not _candidato_es_via(candidato):
                    return None
                location_kind = "approximate_street"
                is_approximate = True
                precision_message = "No se encontró el número exacto. Este punto corresponde a la vía, no necesariamente al inmueble; las distancias serán aproximadas."
        else:
            if numero_candidato:
                # Si el usuario buscó la vía sin número, no sustituirla por una vivienda concreta.
                return None
            location_kind = "approximate_street"
            is_approximate = True
            precision_message = "Este resultado representa la vía y no una dirección predial exacta. Las distancias serán aproximadas."

    return {
        "id": candidate_id,
        "name": _nombre_candidato(candidato),
        "display_name": display_name,
        "latitude": latitude,
        "longitude": longitude,
        "result_type": _etiqueta_tipo(candidato),
        "location_kind": location_kind,
        "is_approximate": is_approximate,
        "precision_message": precision_message,
    }



_PREFIJO_RESIDENCIAL_RE = re.compile(
    r"^\s*(?:(?:urbanizaci[oó]n|unidad\s+residencial|unidad\s+cerrada|"
    r"conjunto\s+residencial|conjunto\s+cerrado|conjunto|unidad|"
    r"parcelaci[oó]n|condominio|residencial)\s*)+",
    re.IGNORECASE,
)


def _nombre_sin_tipo_residencial(consulta):
    """Retira etiquetas genéricas para volver a buscar el nombre propio."""
    nombre = re.sub(r"\s+", " ", consulta or "").strip(" ,-")
    anterior = None
    while nombre and nombre != anterior:
        anterior = nombre
        nombre = _PREFIJO_RESIDENCIAL_RE.sub("", nombre, count=1).strip(" ,-")
    return nombre

def geocodificar_direccion(municipio, consulta):
    """Busca por dirección o lugar usando variantes, y devuelve candidatos confirmables."""
    municipio_canonico = _canonizar_municipio(municipio)
    if not municipio_canonico:
        raise ValueError("El municipio no está disponible para la búsqueda.")
    if not isinstance(consulta, str) or len(consulta.strip()) < 3:
        raise ValueError("Escribe una dirección o el nombre de un lugar (mínimo 3 caracteres).")

    consulta = re.sub(r"\s+", " ", consulta).strip()
    if len(consulta) > 250:
        raise ValueError("La búsqueda es demasiado larga.")

    direccion = _consulta_es_direccion(consulta)
    candidatos = []
    vistos = set()

    # Para lugares como universidades, clínicas, centros comerciales y edificios,
    # probar la búsqueda contextual primero y luego variantes progresivamente
    # más amplias. Cada llamada pasa por caché y límite de 1 solicitud/segundo.
    for variante in range(4):
        parametros = _parametros_texto_libre(consulta, municipio_canonico, variante)
        resultados = _buscar_nominatim(parametros)
        candidatos_encontrados = []

        for resultado in resultados:
            convertido = _convertir_candidato(
                resultado, municipio_canonico, consulta, direccion
            )
            if convertido and convertido["id"] not in vistos:
                candidatos_encontrados.append(convertido)
                vistos.add(convertido["id"])

        if candidatos_encontrados:
            candidatos.extend(candidatos_encontrados)
            # Si encontramos coincidencias válidas en una variante concreta,
            # no mezclamos resultados de búsquedas más amplias que pueden ser
            # menos relevantes.
            break

    # Fallback solo para direcciones: buscar la vía como una entidad vial
    # cuando Nominatim no devuelve el inmueble exacto.
    if not candidatos and direccion:
        parametros_via = _parametros_via(
            direccion["via_texto"], municipio_canonico
        )
        resultados_via = _buscar_nominatim(parametros_via)

        for resultado in resultados_via:
            if not _coincide_municipio_pais(resultado, municipio_canonico):
                continue
            if _clave_via_candidato(resultado) != direccion["via_clave"]:
                continue
            if not _candidato_es_via(resultado):
                continue
            if (resultado.get("address") or {}).get("house_number"):
                continue

            convertido = _convertir_candidato(
                resultado, municipio_canonico, consulta, direccion
            )
            if convertido and convertido["id"] not in vistos:
                candidatos.append(convertido)
                vistos.add(convertido["id"])

    # Búsqueda ampliada para urbanizaciones/unidades/conjuntos residenciales.
    # Importante: también se ejecuta cuando el usuario YA escribió el prefijo.
    # En ese caso buscamos además el nombre propio sin las palabras genéricas,
    # porque el mapa puede tener registrado solo el nombre de la urbanización.
    if not candidatos and not direccion:
        consulta_normalizada = _normalizar(consulta)
        nombre_base = _nombre_sin_tipo_residencial(consulta)
        nombre_base_norm = _normalizar(nombre_base)

        prefijos_residenciales = (
            "urbanización",
            "unidad residencial",
            "unidad cerrada",
            "conjunto residencial",
            "conjunto cerrado",
            "conjunto",
            "parcelación",
            "condominio",
        )

        consultas_residenciales = []
        if nombre_base and nombre_base_norm != consulta_normalizada:
            # Caso: el usuario escribió "Urbanización Los Pinos" pero el mapa
            # puede tener solo "Los Pinos" como nombre del objeto.
            consultas_residenciales.append(nombre_base)

        for prefijo in prefijos_residenciales:
            if nombre_base:
                consultas_residenciales.append(f"{prefijo} {nombre_base}")

        # Deduplicar conservando el orden. Todos los intentos incluyen municipio
        # y departamento, y cada candidato pasa por validación geográfica.
        consultas_unicas = []
        consultas_vistas = set()
        for termino in consultas_residenciales:
            clave = _normalizar(termino)
            if clave and clave not in consultas_vistas:
                consultas_vistas.add(clave)
                consultas_unicas.append(termino)

        for termino in consultas_unicas:
            parametros = _parametros_texto_libre(termino, municipio_canonico, 0)
            resultados = _buscar_nominatim(parametros)

            for resultado in resultados:
                convertido = _convertir_candidato(
                    resultado,
                    municipio_canonico,
                    termino,
                    direccion=None,
                )
                if convertido and convertido["id"] not in vistos:
                    candidatos.append(convertido)
                    vistos.add(convertido["id"])

            # Si ya hay resultados geográficos verificados, no seguir lanzando
            # consultas redundantes al servicio público.
            if candidatos:
                break

    # Un resultado verificado sigue requiriendo confirmación explícita
    # en Angular; este servicio no decide la ubicación por el usuario.
    return candidatos[:8]

