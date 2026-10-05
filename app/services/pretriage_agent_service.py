import os

from dotenv import load_dotenv
from openai import OpenAI

from app.extensions import db
from app.models.pretriage import Pretriage


load_dotenv()


class PretriageAgentService:

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY no está configurada"
            )

        self.client = OpenAI(api_key=api_key)

    def evaluate(self, id_pretriage):

        # =========================================================
        # 1. BUSCAR EL PRETRIAJE EN LA BASE DE DATOS
        # =========================================================

        pretriage = db.session.get(
            Pretriage,
            id_pretriage
        )

        if pretriage is None:
            raise ValueError(
                "El pretriaje no existe"
            )

        # =========================================================
        # 2. OBTENER LA POBLACIÓN
        # =========================================================

        if pretriage.poblacion is None:
            raise ValueError(
                "El pretriaje no tiene una población seleccionada"
            )

        poblacion = pretriage.poblacion.name

        # =========================================================
        # 3. OBTENER LOS ANTECEDENTES
        # =========================================================

        antecedentes = [
            asociacion.antecedente.name
            for asociacion in pretriage.antecedentes_asociados
            if asociacion.antecedente is not None
        ]

        # No tener antecedentes seleccionados es válido.
        if not antecedentes:
            antecedentes_texto = "No se registraron antecedentes"
        else:
            antecedentes_texto = ", ".join(antecedentes)

        # =========================================================
        # 4. OBTENER LAS BANDERAS ROJAS
        # =========================================================

        banderas = [
            asociacion.red_flag.name
            for asociacion in pretriage.banderas_seleccionadas
            if asociacion.red_flag is not None
        ]

        if not banderas:
            raise ValueError(
                "El pretriaje no tiene banderas rojas seleccionadas"
            )

        banderas_texto = ", ".join(banderas)

        # =========================================================
        # 5. INSTRUCCIONES DEL AGENTE
        # =========================================================

        instructions = """
        Eres un asistente de apoyo al pretriaje basado en criterios de
        Medicina de Urgencias y Emergencias.

        RESPONDE SIEMPRE EN ESPAÑOL.

        Tu función es analizar exclusivamente la información proporcionada
        del paciente y sugerir una prioridad de atención.

        Las prioridades de Urgentia son:

        - alta
        - media_alta
        - media_baja
        - baja

        El sistema utiliza el Emergency Severity Index (ESI) como referencia.

        Estas cuatro categorías son propias de Urgentia y no deben
        presentarse como si fueran niveles oficiales del ESI.

        IMPORTANTE:

        Antes de esta evaluación se ejecutaron reglas determinísticas
        del sistema.

        Ninguna de esas reglas activó una alerta inmediata.

        Esto NO significa que el paciente esté clínicamente estable ni
        permite descartar una condición grave.

        REGLAS:

        - Utiliza únicamente la información proporcionada.

        - No inventes síntomas, antecedentes, signos vitales,
          resultados de exámenes ni información que no haya sido
          proporcionada.

        - No establezcas diagnósticos definitivos.

        - No asumas que la ausencia de un dato significa que el paciente
          no presenta dicho signo o síntoma.

        - Si la información disponible no es suficiente para determinar
          una prioridad con confianza, indícalo explícitamente.

        - Da mayor importancia a las condiciones potencialmente graves
          y a las banderas rojas.

        - No disminuyas una prioridad alta que haya sido establecida
          previamente por reglas determinísticas.

        - Esta evaluación funciona únicamente como apoyo al pretriaje
          y no reemplaza la valoración realizada por personal de salud.

        FUENTES DE REFERENCIA:

        Cuando sea necesario fundamentar una decisión clínica, prioriza
        criterios provenientes de fuentes médicas de alta calidad como:

        - Emergency Severity Index (ESI).
        - American College of Emergency Physicians (ACEP).
        - American Heart Association (AHA).
        - European Resuscitation Council (ERC).
        - Sociedad Española de Medicina de Urgencias y Emergencias (SEMES).
        - UpToDate.
        - DynaMed.
        - Tintinalli's Emergency Medicine.
        - Rosen's Emergency Medicine.
        - Reglas de predicción clínica validadas cuando sean aplicables.

        No utilices blogs, foros, contenido de opinión ni sitios
        comerciales dirigidos al público general como fundamento clínico.

        Si existe incertidumbre o evidencia insuficiente, declara la
        limitación en lugar de inventar una conclusión.

        RESPUESTA:

        Responde de manera clara, breve y estructurada.

        Indica:

        - Prioridad sugerida.
        - Justificación breve.
        - Si existe incertidumbre relevante.

        No escribas una explicación clínica excesivamente extensa.
        """

        # =========================================================
        # 6. CONSTRUIR EL PROMPT
        # =========================================================

        prompt = f"""
        DATOS DEL PRETRIAJE

        ID del pretriaje:
        {id_pretriage}

        Tipo de población:
        {poblacion}

        Antecedentes seleccionados:
        {antecedentes_texto}

        Banderas rojas seleccionadas:
        {banderas_texto}

        Resultado previo de las reglas determinísticas:
        No se activó una regla de alerta inmediata.

        Analiza exclusivamente la información anterior y sugiere
        la prioridad correspondiente.
        """

        # =========================================================
        # 7. ENVIAR LOS DATOS A LA IA
        # =========================================================

        response = self.client.responses.create(
            model="gpt-5.6-luna",
            instructions=instructions,
            input=prompt
        )

        # =========================================================
        # 8. DEVOLVER LA RESPUESTA
        # =========================================================

        return response.output_text