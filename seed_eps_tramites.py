from datetime import datetime, timezone

from app import create_app
from app.extensions import db
from app.models.eps import EPS
from app.models.tramite import Tramite
from app.models.eps_tramite import EPSTramite


app = create_app()

orientaciones = [
    {
        "eps": "SURA",
        "codigo": "renovar-formula",
        "requisitos": [
        "Documento de identidad.",
        "Fórmula médica vigente para varios meses.",
        "Código de tratamiento, si está disponible en la fórmula."
    ],
    "pasos": [
        "Verifica si tu fórmula tiene entregas mensuales pendientes.",
        "Escribe al WhatsApp oficial de EPS SURA: 317 518 02 37.",
        "Selecciona la opción de trámites y medicamentos.",
        "Elige medicamentos y luego renovación mensual de fórmula.",
        "Sigue las indicaciones para gestionar la siguiente entrega.",
        "Si ya finalizó el tratamiento, solicita una cita de seguimiento para que el médico determine si debe continuar."
    ],
    "url_oficial": "https://www.epssura.com/informacion-medicamentos"
    },
    {
    "eps": "SURA",
    "codigo": "autorizacion-examen",
    "requisitos": [
        "Documento de identidad.",
        "Orden médica o solicitud del examen, procedimiento o cirugía.",
        "Historia clínica y soportes médicos, cuando sean necesarios.",
        "Tener los documentos digitalizados si vas a enviar la solicitud por internet."
    ],
    "pasos": [
        "Verifica si tu médico o IPS ya gestionó la autorización.",
        "Si necesitas solicitarla, ingresa a www.epssura.com.",
        "Busca Servicios a un clic, luego Solicitudes y autorizaciones.",
        "Selecciona la opción de autorización de órdenes y solicitudes de servicios.",
        "Inicia sesión y sigue las indicaciones para enviar tu solicitud y los soportes requeridos.",
        "Consulta el estado de la solicitud en los servicios digitales de EPS SURA.",
        "También puedes solicitar orientación mediante el WhatsApp 317 518 02 37, en la opción de autorizaciones en salud."
    ],
    "url_oficial": "https://www.epssura.com/afiliados"
    },
    {
    "eps": "SURA",
    "codigo": "autorizacion-especialista",
    "requisitos": [
        "Documento de identidad.",
        "Orden médica o remisión a la especialidad solicitada.",
        "Historia clínica o soportes médicos, cuando sean requeridos.",
        "Tener los documentos digitalizados si necesitas enviar una solicitud virtual."
    ],
    "pasos": [
        "Verifica en tu IPS básica si la remisión al especialista ya fue gestionada.",
        "Pregunta si la cita puede asignarse directamente o si necesitas una autorización previa.",
        "Si necesitas tramitar la autorización, ingresa al portal oficial de EPS SURA.",
        "Busca Servicios a un clic y selecciona Autorización de órdenes y solicitud de servicios.",
        "Inicia sesión y sigue las indicaciones para enviar la orden médica y los soportes requeridos.",
        "Consulta el estado de la solicitud por los canales oficiales de EPS SURA.",
        "Cuando corresponda, solicita la asignación de la cita con el especialista en la IPS indicada."
    ],
    "url_oficial": "https://www.epssura.com/index.php/soluciones-digitales-citas-turnos"
    },
    {
    "eps": "SURA",
    "codigo": "asignacion-cita",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Estar afiliado a EPS SURA y conocer la IPS básica asignada.",
        "Tener disponibles los datos de acceso a los servicios digitales de SURA, si se solicita la cita por internet.",
        "Si se trata de una consulta con especialista, verificar si se requiere remisión u orden médica."
    ],
    "pasos": [
        "Ingresa al portal oficial de EPS SURA.",
        "Busca la sección Citas y turnos.",
        "Selecciona la opción de solicitud de cita con médico general.",
        "Inicia sesión si el portal lo solicita y responde las preguntas necesarias para gestionar tu cita.",
        "Sigue las instrucciones para consultar las opciones de agendamiento disponibles.",
        "Confirma la fecha, hora y lugar de atención que te asigne el sistema.",
        "Si no puedes solicitar la cita por internet, comunícate con tu IPS básica asignada.",
        "Si necesitas una cita con especialista, consulta el canal de asignación correspondiente a tu remisión."
    ],
    "url_oficial": "https://www.epssura.com/index.php/soluciones-digitales-citas-turnos"
    },
    {
    "eps": "SURA",
    "codigo": "vencimiento-examen",
    "requisitos": [
        "Documento de identidad.",
        "Orden médica del examen, procedimiento o cirugía.",
        "Fecha de expedición y vencimiento de la orden.",
        "Historia clínica y soportes médicos relacionados, si los solicitan.",
        "Información de la autorización o cita, si ya fue asignada."
    ],
    "pasos": [
        "Revisa la fecha de vigencia indicada en tu orden o autorización.",
        "Comunícate con la IPS donde te realizarán el servicio para confirmar si la orden todavía puede utilizarse.",
        "Si la orden ya no es válida, consulta con tu IPS básica o con EPS SURA si necesitas una actualización administrativa o una nueva valoración médica.",
        "Ten disponibles la orden anterior y los soportes clínicos para que puedan revisar tu caso.",
        "Si necesitas una nueva autorización, consulta los servicios digitales de EPS SURA y sigue las instrucciones correspondientes.",
        "Si se trata de una cirugía o procedimiento programado, confirma con el prestador la vigencia de la autorización antes de asistir.",
        "Si el examen o procedimiento es necesario para continuar un tratamiento y tienes dificultades para acceder, solicita orientación a tu IPS o EPS."
    ],
    "url_oficial": "https://www.epssura.com/faqs"
    },
    {
    "eps": "SURA",
    "codigo": "vencimiento-especialista",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Orden médica o remisión al especialista.",
        "Fecha de expedición de la orden o remisión.",
        "Autorización anterior, si fue emitida.",
        "Historia clínica o soportes médicos, cuando sean requeridos."
    ],
    "pasos": [
        "Revisa si el documento vencido es la orden médica, la remisión o la autorización.",
        "Comunícate con tu IPS básica o con la institución donde solicitarás la cita para verificar si el documento todavía es válido.",
        "Si la orden o remisión ya no es válida, pregunta si necesitas una nueva valoración médica para actualizarla.",
        "Si tienes una autorización vencida, consulta con EPS SURA si corresponde solicitar una nueva autorización.",
        "Ten disponibles la orden anterior, la autorización y los soportes médicos relacionados.",
        "Cuando tengas los documentos vigentes que correspondan, solicita la asignación de la cita con el especialista por el canal indicado.",
        "Si tienes dificultades para continuar tu atención, solicita orientación a tu IPS o a EPS SURA."
    ],
    "url_oficial": "https://www.epssura.com/afiliados"
    },
    {
    "eps": "Sanitas",
    "codigo": "autorizacion-examen",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Orden médica legible del examen, procedimiento o cirugía.",
        "Acceso al correo electrónico o celular registrado para recibir el código de seguridad.",
        "Soportes clínicos adicionales, si son solicitados durante el trámite."
    ],
    "pasos": [
        "Verifica primero si el prestador de salud ya gestionó la autorización.",
        "Ingresa a la Oficina Virtual de EPS Sanitas o abre su aplicación móvil.",
        "Inicia sesión o regístrate con tus datos de afiliación.",
        "Selecciona la opción Autorizaciones.",
        "Diligencia la solicitud y adjunta una fotografía legible de la orden médica.",
        "Completa la validación de seguridad y sigue las instrucciones del sistema.",
        "Consulta la respuesta por los canales virtuales o mediante los datos de contacto registrados.",
        "Como alternativa, escribe al WhatsApp oficial de Ana María: 320 255 0525, y selecciona gestión de autorizaciones."
    ],
    "url_oficial": "https://www.epssanitas.com/usuarios/web/nuevo-portal-eps/noticia-radica-tus-autorizaciones-facilmente"
    },
    {
    "eps": "Sanitas",
    "codigo": "autorizacion-especialista",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Orden médica o remisión al especialista.",
        "Verificar si la orden ya incluye la autorización del servicio.",
        "Fotografía legible de la orden médica, si necesitas radicarla virtualmente.",
        "Acceso al correo electrónico o celular registrado para recibir códigos de seguridad."
    ],
    "pasos": [
        "Revisa la orden médica entregada por tu médico general y verifica si requiere autorización.",
        "Si la consulta ya está autorizada, identifica el prestador asignado y solicita la cita directamente.",
        "Si necesitas autorización, ingresa a la Oficina Virtual de EPS Sanitas o utiliza su aplicación móvil.",
        "Inicia sesión y selecciona la opción Autorizaciones.",
        "Diligencia la solicitud y adjunta una fotografía legible de la orden médica.",
        "Completa la validación de seguridad y envía la solicitud.",
        "Consulta el estado de la autorización mediante los canales oficiales.",
        "También puedes comunicarte con Ana María, el asistente virtual de Sanitas, por WhatsApp al 320 255 0525.",
        "Cuando obtengas la autorización, solicita la cita con el especialista en la institución correspondiente."
    ],
    "url_oficial": "https://www.epssanitas.com/usuarios/web/nuevo-portal-eps/noticia-radica-tus-autorizaciones-facilmente"
    },
    {
    "eps": "Sanitas",
    "codigo": "asignacion-cita",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Conocer el centro médico o IPS asignada.",
        "Tener acceso a la Oficina Virtual o a la aplicación de EPS Sanitas, si deseas solicitar la cita digitalmente.",
        "Tener disponibles tus datos de contacto.",
        "Para consultas especializadas, contar con la orden médica o autorización cuando corresponda."
    ],
    "pasos": [
        "Ingresa a la sección Citas Médicas del portal oficial de EPS Sanitas.",
        "Selecciona Oficina Virtual de Afiliados o utiliza la aplicación móvil EPS Sanitas.",
        "Inicia sesión y busca la opción de citas médicas.",
        "Selecciona el tipo de consulta y sigue las instrucciones para solicitar la cita.",
        "También puedes solicitar citas mediante Ana María, el asistente virtual de Sanitas, por WhatsApp al 320 255 0525.",
        "Si tu IPS asignada es un prestador externo, comunícate directamente con esa institución para agendar.",
        "Para citas con otras especialidades, utiliza el número telefónico indicado en tu orden médica.",
        "Confirma la fecha, hora y lugar de atención cuando la cita sea asignada."
    ],
    "url_oficial": "https://www.epssanitas.com/usuarios/web/nuevo-portal-eps/citas-medicas"
    },
    {
    "eps": "Sanitas",
    "codigo": "renovar-formula",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Fórmula médica anterior, si está disponible.",
        "Información de los medicamentos y del tratamiento.",
        "Constancia de novedad de la farmacia, si se requiere reformulación por falta de disponibilidad."
    ],
    "pasos": [
        "Verifica si tu fórmula médica sigue vigente y si tienes entregas pendientes.",
        "Si la fórmula está vencida, solicita una cita médica para que el profesional evalúe la continuidad del tratamiento.",
        "Si la farmacia informa que el medicamento presenta una novedad y requiere reformulación, solicita la constancia correspondiente.",
        "Puedes solicitar orientación mediante Ana María, el asistente virtual de Sanitas, por WhatsApp al 320 255 0525.",
        "También puedes comunicarte con la línea de Sanitas en Medellín: (604) 590 8383, o con la línea nacional 01 8000 919 100.",
        "Asiste a la valoración médica con la fórmula anterior y los soportes disponibles.",
        "Si el profesional emite una nueva fórmula, consulta la farmacia asignada y los requisitos para reclamar los medicamentos."
    ],
    "url_oficial": "https://www.epssanitas.com/usuarios/web/nuevo-portal-eps/medicamentos"
    },
    {
    "eps": "Sanitas",
    "codigo": "vencimiento-examen",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Orden médica del examen, procedimiento o cirugía.",
        "Autorización anterior, si fue emitida.",
        "Fecha de expedición y vencimiento de los documentos.",
        "Historia clínica o soportes médicos, si son solicitados."
    ],
    "pasos": [
        "Identifica si venció la orden médica o la autorización del servicio.",
        "Revisa la fecha de vigencia indicada en cada documento.",
        "Consulta con la IPS donde realizarás el examen, procedimiento o cirugía si los documentos todavía pueden utilizarse.",
        "Si venció la orden médica, solicita orientación en tu centro médico para determinar si necesitas una nueva valoración.",
        "Si venció la autorización, comunícate con EPS Sanitas para consultar si corresponde actualizarla o solicitar una nueva.",
        "Puedes consultar novedades de órdenes y autorizaciones mediante el Asesor de Oficina en Línea de Sanitas.",
        "Ten disponibles la orden anterior y los soportes médicos que te soliciten.",
        "Cuando tengas los documentos válidos, confirma con la IPS la programación del servicio."
    ],
    "url_oficial": "https://www.epssanitas.com/usuarios/web/nuevo-portal-eps/canales-de-acceso"
    },
    {
    "eps": "Sanitas",
    "codigo": "vencimiento-especialista",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Orden médica o remisión al especialista.",
        "Autorización anterior, si fue emitida.",
        "Fecha de expedición y vencimiento de los documentos.",
        "Historia clínica o soportes médicos, cuando sean requeridos."
    ],
    "pasos": [
        "Identifica si venció la orden médica, la remisión o la autorización para la consulta especializada.",
        "Comunícate con el centro médico o IPS donde solicitarás la cita para confirmar la vigencia del documento.",
        "Si la orden o remisión ya no es válida, solicita orientación para determinar si necesitas una nueva valoración médica.",
        "Si venció la autorización, consulta con EPS Sanitas si corresponde actualizarla o tramitar una nueva.",
        "Puedes utilizar la Oficina Virtual de EPS Sanitas para consultar los servicios de autorizaciones disponibles.",
        "También puedes solicitar orientación mediante los canales oficiales de atención de Sanitas.",
        "Ten disponibles la orden anterior, la autorización y los soportes clínicos relacionados.",
        "Cuando tengas los documentos válidos, solicita la cita con el especialista en la institución correspondiente."
    ],
    "url_oficial": "https://www.epssanitas.com/usuarios/web/nuevo-portal-eps/canales-de-acceso"
    },
    {
    "eps": "Nueva EPS",
    "codigo": "autorizacion-examen",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Orden médica del examen, procedimiento o cirugía.",
        "Historia clínica o soportes adicionales, cuando sean necesarios.",
        "Acceso a Nueva EPS Móvil si deseas realizar la solicitud digitalmente."
    ],
    "pasos": [
        "Verifica primero con tu IPS si la autorización ya fue gestionada o si debes solicitarla.",
        "Si necesitas radicarla, ingresa a la aplicación Nueva EPS Móvil.",
        "Selecciona la opción Autorizaciones y después Solicitar.",
        "Adjunta una fotografía legible de la orden médica y de los soportes disponibles.",
        "Agrega observaciones si necesitas explicar alguna información adicional.",
        "Selecciona Grabar para registrar la solicitud.",
        "Consulta el estado de la autorización en la opción Consulta de la aplicación.",
        "Si no puedes realizar el trámite digitalmente, consulta los canales oficiales de atención de Nueva EPS.",
        "Cuando recibas la autorización, comunícate con la IPS correspondiente para programar el servicio."
    ],
    "url_oficial": "https://nuevaeps.com.co/personas/regimen-contributivo/autorizaciones"
    },
    {
    "eps": "Nueva EPS",
    "codigo": "autorizacion-especialista",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Orden médica o remisión para valoración con especialista.",
        "Soportes clínicos adicionales, cuando sean solicitados.",
        "Acceso a la aplicación Nueva EPS Móvil, si necesitas radicar una autorización digitalmente."
    ],
    "pasos": [
        "Revisa la orden médica e identifica la especialidad solicitada.",
        "Consulta con tu IPS si la autorización ya fue gestionada o si debes solicitarla.",
        "Si necesitas tramitarla personalmente, ingresa a la aplicación Nueva EPS Móvil.",
        "Selecciona Autorizaciones y luego Solicitar.",
        "Adjunta una fotografía legible de la orden médica y los soportes disponibles.",
        "Agrega observaciones si necesitas proporcionar información adicional.",
        "Selecciona Grabar para registrar la solicitud.",
        "Consulta la respuesta en la sección Autorizaciones y luego Consultar.",
        "Cuando tengas la autorización o el direccionamiento correspondiente, comunícate con la IPS indicada para solicitar la cita.",
        "Si tienes dificultades, consulta los canales oficiales de Nueva EPS para recibir orientación."
    ],
    "url_oficial": "https://nuevaeps.com.co/personas/regimen-contributivo/autorizaciones"
    },
    {
    "eps": "Nueva EPS",
    "codigo": "asignacion-cita",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Conocer la IPS primaria asignada.",
        "Tener disponibles los datos de contacto.",
        "Si se trata de una consulta especializada, contar con la remisión o autorización correspondiente, cuando aplique."
    ],
    "pasos": [
        "Identifica tu IPS primaria asignada.",
        "Comunícate telefónicamente con tu IPS o acércate presencialmente para solicitar una cita de medicina general.",
        "También puedes ingresar a la aplicación Nueva EPS Móvil y buscar la opción Citas Médicas.",
        "Selecciona el paciente y consulta las fechas disponibles, si tu IPS permite el agendamiento por la aplicación.",
        "Selecciona la fecha y hora y confirma la cita.",
        "Si no encuentras disponibilidad en la aplicación, comunícate directamente con tu IPS.",
        "Si no sabes cuál es tu IPS, consulta los canales oficiales de Nueva EPS para identificarla.",
        "Si necesitas una cita con especialista, revisa la remisión y comunícate con la institución indicada para solicitarla.",
        "Confirma la fecha, hora y lugar de atención y lleva tu documento de identidad."
    ],
    "url_oficial": "https://nuevaeps.com.co/personas/regimen-subsidiado/citas-medicas"
    },
    {
    "eps": "Nueva EPS",
    "codigo": "renovar-formula",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Fórmula médica anterior o vigente, según el caso.",
        "Información del medicamento y del tratamiento.",
        "Orden o autorización de entregas pendientes, si está disponible."
    ],
    "pasos": [
        "Revisa la fecha de vigencia de tu fórmula médica.",
        "Comprueba si tienes entregas mensuales pendientes de un tratamiento formulado para varios meses.",
        "Si tienes entregas pendientes y la orden está vigente, consulta con tu gestor farmacéutico cómo solicitar la siguiente entrega.",
        "Si la fórmula está vencida o el tratamiento terminó, solicita una nueva cita médica para que el profesional evalúe su continuidad.",
        "Lleva a la consulta la fórmula anterior y la información de los medicamentos que utilizas.",
        "Si el médico expide una nueva fórmula, verifica su vigencia y las autorizaciones necesarias, cuando correspondan.",
        "Consulta en el portal oficial de Nueva EPS el gestor farmacéutico asignado a tu IPS y municipio.",
        "Acude al punto de dispensación correspondiente con los documentos requeridos."
    ],
    "url_oficial": "https://nuevaeps.com.co/paso_a_paso_colsubsidio"
    },
    {
    "eps": "Nueva EPS",
    "codigo": "vencimiento-examen",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Orden médica del examen, procedimiento o cirugía.",
        "Autorización anterior, si fue emitida.",
        "Fecha de expedición y vencimiento de los documentos.",
        "Historia clínica y soportes médicos, cuando sean requeridos."
    ],
    "pasos": [
        "Identifica si venció la orden médica o la autorización del servicio.",
        "Revisa la fecha de vigencia que aparece en la parte inferior de la orden.",
        "Comunícate con la IPS donde realizarás el examen, procedimiento o cirugía para confirmar si los documentos todavía son válidos.",
        "Si venció la orden médica, consulta con tu IPS primaria si necesitas una nueva valoración para actualizarla.",
        "Si venció la autorización, comunícate con Nueva EPS para consultar si corresponde solicitar una nueva.",
        "Ten disponibles la orden anterior y los soportes clínicos relacionados.",
        "Si necesitas tramitar una autorización, consulta los canales oficiales de Nueva EPS o las opciones disponibles en Nueva EPS Móvil.",
        "Cuando tengas los documentos válidos, confirma con la IPS la programación del servicio."
    ],
    "url_oficial": "https://nuevaeps.com.co/personas/regimen-contributivo/autorizaciones"
    },
    {
    "eps": "Nueva EPS",
    "codigo": "vencimiento-especialista",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Orden médica o remisión para valoración con especialista.",
        "Autorización anterior, si fue emitida.",
        "Fecha de expedición y vencimiento de los documentos.",
        "Historia clínica o soportes médicos, cuando sean requeridos."
    ],
    "pasos": [
        "Identifica si venció la orden médica, la remisión o la autorización para la consulta especializada.",
        "Revisa las fechas de vigencia indicadas en los documentos.",
        "Comunícate con tu IPS primaria o con la institución donde solicitarás la cita para confirmar si los documentos todavía son válidos.",
        "Si la orden o remisión ya no es válida, pregunta en tu IPS si necesitas una nueva valoración médica.",
        "Si venció la autorización, consulta con Nueva EPS si corresponde actualizarla o tramitar una nueva.",
        "Si perteneces al régimen contributivo y necesitas una autorización, consulta las opciones disponibles en Nueva EPS Móvil.",
        "Si perteneces al régimen subsidiado, consulta con tu IPS o los canales de Nueva EPS cómo gestionar la solicitud.",
        "Ten disponibles la orden anterior, la autorización y los soportes médicos relacionados.",
        "Cuando tengas los documentos válidos, comunícate con la IPS correspondiente para solicitar la cita con el especialista.",
        "Si tienes dificultades para continuar tu atención, solicita orientación a Nueva EPS por sus canales oficiales."
    ],
    "url_oficial": "https://nuevaeps.com.co/personas/regimen-contributivo/autorizaciones"
    },
    {
    "eps": "Salud Total",
    "codigo": "autorizacion-examen",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Orden médica del examen, procedimiento o cirugía.",
        "Historia clínica y soportes médicos, cuando sean requeridos.",
        "Datos de acceso a la Oficina Virtual, si vas a utilizar ese canal."
    ],
    "pasos": [
        "Verifica con la IPS si el servicio ya fue autorizado o si debes solicitar la autorización.",
        "Ingresa al sitio oficial de Salud Total EPS.",
        "Busca la opción Oficina Virtual e inicia sesión como afiliado.",
        "Consulta el módulo de autorizaciones y las opciones de solicitud disponibles.",
        "Si el sistema permite radicar tu solicitud, adjunta la orden médica y los soportes requeridos.",
        "Guarda el número de radicado o comprobante que genere el sistema.",
        "Consulta el estado de tu solicitud en la Oficina Virtual.",
        "Si no encuentras la opción correspondiente, solicita orientación directamente a Salud Total o a tu IPS.",
        "Una vez autorizado el servicio, confirma con el prestador cómo programarlo."
    ],
    "url_oficial": "https://www.saludtotal.com.co/"
    },
    {
    "eps": "Salud Total",
    "codigo": "autorizacion-especialista",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Orden médica o remisión para valoración con especialista.",
        "Historia clínica o soportes médicos, cuando sean requeridos.",
        "Datos de acceso a la Oficina Virtual, si utilizarás el canal digital."
    ],
    "pasos": [
        "Revisa la orden médica e identifica la especialidad solicitada.",
        "Consulta con tu IPS si el servicio ya tiene autorización o direccionamiento.",
        "Si ya tienes el direccionamiento, verifica cuál es la institución asignada para solicitar la cita.",
        "Si necesitas gestionar el servicio, ingresa al portal oficial de Salud Total EPS.",
        "Accede a la Oficina Virtual e identifica las opciones de Direccionamientos o Radicación de solicitudes disponibles para tu usuario.",
        "Sigue las indicaciones del portal y presenta la orden médica y los soportes solicitados.",
        "Conserva el comprobante o número de radicado, si el sistema lo genera.",
        "Consulta el estado de tu solicitud mediante los canales oficiales de Salud Total.",
        "Cuando tengas el direccionamiento correspondiente, comunícate con la IPS indicada para solicitar la cita con el especialista.",
        "Si tienes dificultades para gestionar el servicio, solicita orientación a tu IPS o a Salud Total."
    ],
    "url_oficial": "https://www.saludtotal.com.co/"
    },
    {
    "eps": "Salud Total",
    "codigo": "asignacion-cita",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Conocer la IPS primaria asignada.",
        "Tener disponibles los datos de contacto.",
        "Si se trata de una consulta especializada, contar con la remisión o el direccionamiento correspondiente, cuando aplique."
    ],
    "pasos": [
        "Identifica la IPS primaria que tienes asignada en Salud Total.",
        "Ingresa al portal oficial de Salud Total EPS.",
        "Busca la Oficina Virtual y consulta las opciones disponibles para solicitar citas médicas.",
        "Si tu IPS permite el agendamiento digital, selecciona el servicio y sigue las instrucciones del sistema.",
        "También puedes consultar las opciones de citas en la aplicación oficial de Salud Total EPS.",
        "Si no encuentras disponibilidad o tu IPS no permite agendar por internet, comunícate directamente con la institución asignada.",
        "Para una consulta con especialista, verifica si necesitas una remisión o un direccionamiento previo.",
        "Confirma la fecha, hora, lugar de atención y documentos necesarios para asistir."
    ],
    "url_oficial": "https://www.saludtotal.com.co/"
    },
    {
    "eps": "Salud Total",
    "codigo": "renovar-formula",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Fórmula médica anterior o vigente, según el caso.",
        "Información de los medicamentos y del tratamiento.",
        "Autorización o comprobante de entregas pendientes, si está disponible."
    ],
    "pasos": [
        "Revisa la fecha de vigencia de tu fórmula médica y comprueba si tienes entregas pendientes.",
        "Si tu fórmula sigue vigente y tienes entregas pendientes, consulta con el gestor farmacéutico asignado cómo solicitar la siguiente entrega.",
        "Si tu fórmula venció o el tratamiento terminó, solicita una cita médica para que el profesional evalúe si necesitas una nueva prescripción.",
        "Ingresa al portal oficial de Salud Total EPS para consultar los canales disponibles de citas y medicamentos.",
        "Si necesitas una nueva valoración, lleva la fórmula anterior y la información de los medicamentos que utilizas.",
        "Cuando el profesional emita una nueva fórmula, verifica si necesitas autorización o direccionamiento para reclamar los medicamentos.",
        "Consulta cuál es el gestor farmacéutico asignado y los documentos necesarios para la dispensación.",
        "Si tienes dificultades con la entrega o continuidad del tratamiento, solicita orientación a Salud Total por sus canales oficiales."
    ],
    "url_oficial": "https://www.saludtotal.com.co/"
    },
    {
    "eps": "Salud Total",
    "codigo": "vencimiento-examen",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Orden médica del examen, procedimiento o cirugía.",
        "Autorización anterior, si fue emitida.",
        "Fecha de expedición y vencimiento de los documentos.",
        "Historia clínica y soportes médicos, cuando sean requeridos."
    ],
    "pasos": [
        "Identifica si venció la orden médica o la autorización del servicio.",
        "Revisa las fechas de vigencia indicadas en los documentos.",
        "Comunícate con la IPS donde realizarás el examen, procedimiento o cirugía para verificar si los documentos todavía pueden utilizarse.",
        "Si venció la orden médica, consulta con tu IPS primaria si necesitas una nueva valoración para obtener una orden actualizada.",
        "Si venció la autorización, solicita orientación a Salud Total para determinar si corresponde actualizarla o tramitar una nueva.",
        "Ten disponibles la orden anterior, la autorización y los soportes clínicos relacionados.",
        "Consulta los canales de atención de Salud Total para conocer las opciones disponibles de autorizaciones.",
        "Si el procedimiento ya estaba programado, confirma con la IPS qué documentos necesitas antes de asistir.",
        "Cuando tengas los documentos válidos, continúa con la programación del servicio."
    ],
    "url_oficial": "https://www.saludtotal.com.co/"
    },
    {
    "eps": "Salud Total",
    "codigo": "vencimiento-especialista",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Orden médica o remisión anterior para valoración con especialista.",
        "Autorización o direccionamiento anterior, si fue emitido.",
        "Fecha de expedición y vencimiento de los documentos.",
        "Historia clínica y soportes médicos, cuando sean requeridos."
    ],
    "pasos": [
        "Revisa la remisión médica y verifica su fecha de expedición y vigencia.",
        "Identifica si venció la remisión médica o la autorización o direccionamiento del servicio.",
        "Consulta con la IPS asignada si la remisión todavía puede utilizarse para solicitar la cita.",
        "Si la remisión médica está vencida, pregunta a tu IPS primaria si necesitas una nueva valoración médica.",
        "Si venció la autorización o el direccionamiento, solicita orientación a Salud Total para conocer si corresponde actualizarlo o gestionar uno nuevo.",
        "Ingresa al portal oficial de Salud Total EPS para consultar los canales de atención disponibles.",
        "Ten disponibles la remisión anterior, la autorización y los soportes médicos relacionados.",
        "Si ya tenías una cita programada, comunícate con la IPS para verificar si debes actualizar algún documento.",
        "Cuando tengas una remisión y un direccionamiento válidos, según corresponda, solicita la cita con el especialista en la IPS indicada.",
        "Si tienes dificultades para continuar el trámite, comunícate con Salud Total para recibir orientación."
    ],
    "url_oficial": "https://www.saludtotal.com.co/"
    },
    {
    "eps": "Coosalud",
    "codigo": "autorizacion-examen",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Orden médica del examen, procedimiento o cirugía.",
        "Historia clínica y soportes médicos, cuando sean requeridos.",
        "Datos de acceso al portal de afiliados, si corresponde realizar una solicitud digital."
    ],
    "pasos": [
        "Revisa la orden médica e identifica el examen, procedimiento o cirugía solicitado.",
        "Consulta primero con la IPS si el servicio se gestiona directamente entre la institución y Coosalud.",
        "Si la IPS confirma que debes realizar una solicitud, ingresa al portal oficial de Coosalud.",
        "Busca la sección Tus trámites o el portal de autogestión para afiliados.",
        "Inicia sesión o regístrate si el portal lo requiere.",
        "Consulta si está habilitada la radicación de órdenes médicas para el servicio solicitado.",
        "Si la opción está disponible, sigue las instrucciones del portal y presenta los soportes requeridos.",
        "Guarda el número de caso o comprobante, si el sistema lo genera.",
        "Consulta el estado de la solicitud mediante los canales oficiales de Coosalud.",
        "Cuando la IPS confirme que el servicio puede programarse, solicita la fecha y las indicaciones correspondientes."
    ],
    "url_oficial": "https://coosalud.com/"

    },
    {
    "eps": "Coosalud",
    "codigo": "autorizacion-especialista",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Orden médica o remisión para consulta con especialista, cuando corresponda.",
        "Historia clínica o soportes médicos, si son requeridos.",
        "Datos de acceso al portal de afiliados, si se necesita radicar una solicitud digital."
    ],
    "pasos": [
        "Revisa la orden médica e identifica la especialidad solicitada.",
        "Consulta con tu IPS si la remisión se gestiona directamente entre la institución y Coosalud.",
        "Verifica si ya existe un direccionamiento hacia una IPS especializada.",
        "Si la IPS indica que debes realizar una solicitud, ingresa al portal oficial de Coosalud.",
        "Busca la sección Tus trámites y consulta las opciones disponibles para radicar órdenes médicas.",
        "Si el portal permite gestionar tu solicitud, inicia sesión y adjunta los documentos requeridos.",
        "Guarda el número de caso o comprobante generado, si corresponde.",
        "Consulta el estado de la solicitud mediante los canales oficiales de Coosalud.",
        "Cuando se confirme la institución prestadora asignada, verifica cómo obtener la cita con el especialista.",
        "Si no encuentras la opción digital o tienes dificultades, solicita orientación directamente a Coosalud o a tu IPS."
    ],
    "url_oficial": "https://coosalud.com/"
    },
    {
    "eps": "Coosalud",
    "codigo": "asignacion-cita",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Conocer la IPS primaria asignada.",
        "Tener actualizados los datos de contacto.",
        "Contar con la remisión médica si se solicita una consulta especializada que la requiera."
    ],
    "pasos": [
        "Identifica la IPS primaria que tienes asignada en Coosalud.",
        "Verifica si la cita que necesitas corresponde a medicina general o a una consulta especializada.",
        "Para medicina general, consulta los canales de asignación de citas de tu IPS primaria.",
        "Ingresa al portal oficial de Coosalud y busca las opciones de atención al afiliado y trámites.",
        "Consulta si tu IPS dispone de agendamiento por internet, teléfono o atención presencial.",
        "Selecciona el canal habilitado y proporciona los datos necesarios para solicitar la cita.",
        "Si necesitas una consulta con especialista, verifica si tu remisión debe gestionarse previamente con la IPS o con Coosalud.",
        "Confirma la fecha, hora, lugar de atención y documentos que debes presentar.",
        "Si no consigues una cita o tienes dificultades con el proceso, solicita orientación a tu IPS o a Coosalud."
    ],
    "url_oficial": "https://coosalud.com/"
    },
    {
    "eps": "Coosalud",
    "codigo": "renovar-formula",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Fórmula médica anterior o vigente.",
        "Información de los medicamentos prescritos y del tratamiento.",
        "Comprobante de dispensación o autorización anterior, si está disponible.",
        "Historia clínica o soportes médicos, cuando sean requeridos."
    ],
    "pasos": [
        "Revisa la fecha de expedición y la vigencia de tu fórmula médica.",
        "Verifica si todavía tienes entregas pendientes de medicamentos.",
        "Si la fórmula está vigente y tienes entregas pendientes, consulta con el gestor farmacéutico asignado por Coosalud cómo solicitar la siguiente entrega.",
        "Si la fórmula está vencida, comunícate con tu IPS primaria para solicitar una valoración médica o consultar el procedimiento de renovación que corresponda.",
        "Ingresa al portal oficial de Coosalud para consultar los canales disponibles de atención al afiliado y medicamentos.",
        "Si necesitas una nueva valoración, presenta la fórmula anterior y la información de los medicamentos que utilizas.",
        "Cuando el profesional de salud emita una nueva fórmula, verifica si los medicamentos requieren autorización o direccionamiento.",
        "Consulta cuál es el punto o gestor farmacéutico asignado para reclamar los medicamentos.",
        "Presenta los documentos solicitados y conserva los comprobantes de dispensación.",
        "Si tienes dificultades para recibir los medicamentos o continuar tu tratamiento, solicita orientación a Coosalud mediante sus canales oficiales."
    ],
    "url_oficial": "https://coosalud.com/"
    },
    {
    "eps": "Coosalud",
    "codigo": "vencimiento-examen",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Orden médica anterior del examen, procedimiento o cirugía.",
        "Autorización anterior, si fue emitida.",
        "Fecha de expedición y vencimiento de los documentos.",
        "Historia clínica y soportes médicos, cuando sean requeridos."
    ],
    "pasos": [
        "Identifica si venció la orden médica o la autorización del servicio.",
        "Revisa las fechas de expedición y vigencia de los documentos.",
        "Comunícate con la IPS donde se realizará el examen, procedimiento o cirugía para verificar si los documentos todavía pueden utilizarse.",
        "Si venció la orden médica, consulta con tu IPS primaria si necesitas una nueva valoración médica para obtener una orden actualizada.",
        "Si venció la autorización, pregunta a la IPS si puede gestionar su actualización directamente con Coosalud.",
        "Si la IPS indica que debes realizar el trámite, consulta los canales oficiales de Coosalud para conocer el procedimiento correspondiente.",
        "Ten disponibles la orden anterior, la autorización y los soportes clínicos relacionados.",
        "Si el procedimiento ya estaba programado, confirma con la IPS si necesitas actualizar algún documento antes de asistir.",
        "Cuando cuentes con los documentos válidos, según corresponda, continúa con la programación del servicio.",
        "Si tienes dificultades para gestionar el trámite, solicita orientación a Coosalud o a tu IPS."
    ],
    "url_oficial": "https://coosalud.com/"
    },
    {
    "eps": "Coosalud",
    "codigo": "vencimiento-especialista",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Orden médica o remisión anterior para valoración con especialista.",
        "Autorización o direccionamiento anterior, si fue emitido.",
        "Fecha de expedición y vencimiento de los documentos.",
        "Historia clínica y soportes médicos, cuando sean requeridos."
    ],
    "pasos": [
        "Revisa la remisión médica y verifica su fecha de expedición y vigencia.",
        "Identifica si venció la remisión médica o la autorización o direccionamiento del servicio.",
        "Consulta con tu IPS si la remisión todavía puede utilizarse para solicitar la cita.",
        "Si la remisión está vencida, pregunta a tu IPS primaria si necesitas una nueva valoración médica.",
        "Si venció la autorización o el direccionamiento, consulta con la IPS si puede gestionar su actualización directamente con Coosalud.",
        "Si la IPS indica que debes realizar una solicitud, ingresa al portal oficial de Coosalud y consulta los canales de atención disponibles.",
        "Ten disponibles la remisión anterior, la autorización y los soportes médicos relacionados.",
        "Si ya tenías una cita programada, comunícate con la IPS para verificar si necesitas actualizar algún documento.",
        "Cuando tengas los documentos válidos, según corresponda, confirma con la IPS cómo solicitar o mantener la cita con el especialista.",
        "Si tienes dificultades para continuar el trámite, solicita orientación a Coosalud o a tu IPS."
    ],
    "url_oficial": "https://coosalud.com/"
    },
    {
    "eps": "Savia Salud",
    "codigo": "autorizacion-examen",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Orden médica del examen, procedimiento o cirugía.",
        "Historia clínica y soportes médicos correspondientes.",
        "Anexo de solicitud de autorización, cuando sea requerido.",
        "Datos de contacto actualizados para recibir información."
    ],
    "pasos": [
        "Revisa la orden médica e identifica el servicio solicitado.",
        "Consulta con tu IPS si puede gestionar la autorización directamente ante Savia Salud.",
        "Si necesitas realizar el trámite personalmente, ingresa al portal oficial de autorizaciones de Savia Salud.",
        "Selecciona la opción Solicitud de autorizaciones.",
        "Diligencia los datos solicitados y adjunta la orden médica y los soportes requeridos.",
        "Envía la solicitud y conserva el comprobante o número de radicado, si se genera.",
        "Utiliza la opción Consulta el estado de tu solicitud para verificar el avance del trámite.",
        "Cuando la autorización esté disponible, consulta o descarga el documento desde el portal.",
        "Comunícate con la IPS indicada para confirmar la programación del examen, procedimiento o cirugía.",
        "Si no puedes realizar el trámite digitalmente, acude a un punto de atención de Savia Salud o solicita orientación en la línea nacional 018000423683."
    ],
    "url_oficial": "https://www.saviasaludeps.com/sitioweb/component/sppagebuilder/page/288"
    },
    {
    "eps": "Savia Salud",
    "codigo": "autorizacion-especialista",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Orden médica o remisión para valoración con especialista.",
        "Historia clínica y soportes médicos correspondientes.",
        "Anexo de solicitud de autorización, cuando sea requerido.",
        "Datos de contacto actualizados."
    ],
    "pasos": [
        "Revisa la orden médica e identifica la especialidad solicitada.",
        "Consulta con tu IPS si puede gestionar directamente la autorización ante Savia Salud.",
        "Si necesitas realizar la solicitud personalmente, ingresa al portal oficial de autorizaciones de Savia Salud.",
        "Selecciona la opción Solicitud de autorizaciones.",
        "Diligencia los datos solicitados y adjunta la remisión médica y los soportes requeridos.",
        "Envía la solicitud y conserva el número de radicado o comprobante, si se genera.",
        "Utiliza la opción Consulta el estado de tu solicitud para verificar el avance del trámite.",
        "Cuando la autorización esté disponible, consulta o descarga el documento desde el portal.",
        "Verifica la IPS o institución especializada a la que fue direccionado el servicio.",
        "Comunícate con la IPS indicada para solicitar la cita con el especialista.",
        "Si tienes dificultades con el trámite, solicita orientación a Savia Salud en la línea nacional 018000423683 o en un punto de atención."
    ],
    "url_oficial": "https://www.saviasaludeps.com/sitioweb/component/sppagebuilder/page/288"
    },
    {
    "eps": "Savia Salud",
    "codigo": "asignacion-cita",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Conocer la IPS primaria asignada.",
        "Tener actualizados los datos de contacto.",
        "Contar con una remisión o autorización si se solicita una consulta especializada que la requiera."
    ],
    "pasos": [
        "Identifica la IPS primaria que tienes asignada en Savia Salud.",
        "Verifica si la cita que necesitas corresponde a medicina general o a una consulta especializada.",
        "Para medicina general, comunícate con tu IPS primaria y consulta los canales disponibles para solicitar citas.",
        "Ingresa al portal oficial de Savia Salud para consultar información sobre la red de atención y los canales de servicio.",
        "Si tu IPS permite el agendamiento por teléfono, internet o atención presencial, utiliza el canal correspondiente.",
        "Proporciona tus datos de identificación y solicita la fecha disponible para la consulta.",
        "Si necesitas una consulta con especialista, verifica previamente si debes gestionar una remisión o autorización.",
        "Confirma la fecha, hora, lugar de atención y documentos que debes presentar.",
        "Si tienes dificultades para conseguir la cita, solicita orientación a tu IPS o a Savia Salud por sus canales oficiales."
    ],
    "url_oficial": "https://www.saviasaludeps.com/"
    },
    {
    "eps": "Savia Salud",
    "codigo": "renovar-formula",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Fórmula médica anterior o vigente.",
        "Información de los medicamentos prescritos y del tratamiento.",
        "Comprobante de dispensación o autorización anterior, si está disponible.",
        "Historia clínica o soportes médicos, cuando sean requeridos."
    ],
    "pasos": [
        "Revisa la fecha de expedición y vigencia de tu fórmula médica.",
        "Verifica si tienes entregas pendientes de medicamentos.",
        "Si la fórmula está vigente y tienes entregas pendientes, consulta con el operador farmacéutico asignado cómo solicitar la siguiente entrega.",
        "Si la fórmula está vencida, comunícate con tu IPS primaria para consultar si necesitas una nueva valoración médica.",
        "Ingresa al portal oficial de Savia Salud para consultar los canales de atención y orientación sobre medicamentos.",
        "Si necesitas una nueva valoración, presenta la fórmula anterior y la información de los medicamentos que utilizas.",
        "Cuando el profesional de salud emita una nueva fórmula, verifica si los medicamentos requieren autorización o direccionamiento.",
        "Consulta el punto de dispensación asignado para reclamar los medicamentos.",
        "Presenta los documentos solicitados y conserva los comprobantes de entrega.",
        "Si tienes dificultades para acceder a los medicamentos o continuar el tratamiento, solicita orientación a Savia Salud o a tu IPS."
    ],
    "url_oficial": "https://www.saviasaludeps.com/"
    },
    {
    "eps": "Savia Salud",
    "codigo": "vencimiento-examen",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Orden médica anterior del examen, procedimiento o cirugía.",
        "Autorización anterior, si fue emitida.",
        "Fecha de expedición y vencimiento de los documentos.",
        "Historia clínica y soportes médicos, cuando sean requeridos."
    ],
    "pasos": [
        "Identifica si venció la orden médica o la autorización del servicio.",
        "Revisa las fechas de expedición y vigencia indicadas en los documentos.",
        "Comunícate con la IPS donde se realizará el examen, procedimiento o cirugía para verificar si los documentos todavía pueden utilizarse.",
        "Si venció la orden médica, consulta con tu IPS primaria si necesitas una nueva valoración médica para obtener una orden actualizada.",
        "Si venció la autorización, consulta con la IPS si puede gestionar su actualización directamente ante Savia Salud.",
        "Si necesitas realizar una solicitud personalmente, ingresa al portal oficial de autorizaciones de Savia Salud.",
        "Consulta las opciones de solicitud y seguimiento disponibles para tu caso.",
        "Ten disponibles la orden anterior, la autorización y los soportes clínicos relacionados.",
        "Si el procedimiento ya estaba programado, confirma con la IPS si debes actualizar algún documento antes de asistir.",
        "Cuando tengas los documentos válidos, según corresponda, continúa con la programación del servicio.",
        "Si tienes dificultades para gestionar el trámite, solicita orientación a Savia Salud o a tu IPS."
    ],
    "url_oficial": "https://www.saviasaludeps.com/sitioweb/component/sppagebuilder/page/288"
    },
    {
    "eps": "Savia Salud",
    "codigo": "vencimiento-especialista",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Orden médica o remisión anterior para valoración con especialista.",
        "Autorización o direccionamiento anterior, si fue emitido.",
        "Fecha de expedición y vencimiento de los documentos.",
        "Historia clínica y soportes médicos, cuando sean requeridos."
    ],
    "pasos": [
        "Revisa la remisión médica y verifica su fecha de expedición y vigencia.",
        "Identifica si venció la remisión médica o la autorización o direccionamiento del servicio.",
        "Consulta con tu IPS si la remisión todavía puede utilizarse para solicitar la cita.",
        "Si la remisión está vencida, pregunta a tu IPS primaria si necesitas una nueva valoración médica.",
        "Si venció la autorización o el direccionamiento, consulta con la IPS si puede gestionar su actualización directamente ante Savia Salud.",
        "Si necesitas realizar una solicitud personalmente, ingresa al portal oficial de autorizaciones de Savia Salud.",
        "Consulta las opciones disponibles de solicitud y seguimiento para tu caso.",
        "Ten disponibles la remisión anterior, la autorización y los soportes médicos relacionados.",
        "Si ya tenías una cita programada, comunícate con la IPS para verificar si necesitas actualizar algún documento.",
        "Cuando tengas los documentos válidos, según corresponda, confirma con la IPS cómo solicitar o mantener la cita con el especialista.",
        "Si tienes dificultades para continuar el trámite, solicita orientación a Savia Salud o a tu IPS."
    ],
    "url_oficial": "https://www.saviasaludeps.com/sitioweb/component/sppagebuilder/page/288"
    },
    {
    "eps": "Compensar",
    "codigo": "autorizacion-examen",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Orden médica del examen, procedimiento o cirugía.",
        "Historia clínica y soportes médicos, cuando sean requeridos.",
        "Información de la IPS que emitió la orden.",
        "Datos de acceso a los canales digitales de Compensar, si corresponde."
    ],
    "pasos": [
        "Revisa la orden médica e identifica el examen, procedimiento o cirugía solicitado.",
        "Consulta con tu IPS si el servicio requiere autorización y si la institución realiza directamente la gestión.",
        "Si necesitas gestionar la autorización, ingresa a la Ruta de Servicios oficial de Compensar EPS.",
        "Busca la sección Gestión de trámites y selecciona Autorizaciones.",
        "Consulta los canales habilitados para autorizar órdenes médicas del Plan de Beneficios en Salud (PBS).",
        "Sigue las instrucciones del canal correspondiente y presenta la orden médica y los soportes solicitados.",
        "Conserva el número de solicitud o comprobante, si se genera.",
        "Consulta el estado de la autorización por los canales oficiales de Compensar.",
        "Cuando se confirme la autorización, verifica cuál es la IPS asignada para realizar el servicio.",
        "Comunícate con la IPS para confirmar la programación del examen, procedimiento o cirugía.",
        "Si tienes dificultades, solicita orientación a Compensar EPS o a tu IPS."
    ],
    "url_oficial": "https://corporativo.compensar.com/salud/plan-de-beneficios-en-salud/compensar-eps/ruta-de-servicios"
    },
    {
    "eps": "Compensar",
    "codigo": "autorizacion-especialista",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Orden médica o remisión para valoración con especialista, emitida por un profesional de la red de atención de Compensar.",
        "Historia clínica y resultados de exámenes anteriores, cuando sean requeridos.",
        "Datos de contacto actualizados.",
        "Información de la IPS asignada, si ya existe un direccionamiento."
    ],
    "pasos": [
        "Revisa la orden médica e identifica la especialidad solicitada.",
        "Verifica que la orden haya sido emitida por un profesional de la red de atención de Compensar EPS.",
        "Ingresa a la página oficial de citas médicas de Compensar EPS.",
        "Busca la sección Citas con Especialistas y consulta los canales disponibles.",
        "Solicita la asignación de la cita o la autorización del servicio, según lo que requiera tu orden médica.",
        "Si la orden requiere autorización, sigue las indicaciones del canal oficial de Compensar para gestionarla.",
        "Cuando se genere la autorización, verifica cuál es la IPS o el prestador asignado.",
        "Utiliza los canales indicados para solicitar la cita con el especialista.",
        "Confirma la fecha, hora y lugar de atención.",
        "El día de la consulta, lleva tu orden médica y los resultados de exámenes anteriores que tengas.",
        "Si tienes dificultades con la autorización o la cita, solicita orientación a Compensar EPS."
    ],
    "url_oficial": "https://corporativo.compensar.com/salud/compensar-eps/cita-medica"
    },
    {
    "eps": "Compensar",
    "codigo": "asignacion-cita",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Estar afiliado a Compensar EPS.",
        "Tener actualizados los datos de contacto.",
        "Conocer la IPS o sede de atención asignada, si corresponde."
    ],
    "pasos": [
        "Ingresa a la página oficial de citas médicas de Compensar EPS.",
        "Identifica si necesitas una cita de medicina general o una consulta especializada.",
        "Busca la sección de citas de medicina general y consulta los canales de agendamiento disponibles.",
        "Selecciona el canal habilitado para tu servicio, como la plataforma digital o los canales de atención indicados por Compensar.",
        "Identifícate con los datos solicitados por el sistema.",
        "Consulta las fechas, horarios y sedes disponibles para la atención.",
        "Selecciona la cita que se ajuste a tus necesidades y confirma la solicitud.",
        "Guarda el comprobante o la información de la cita, si el sistema lo proporciona.",
        "Verifica la fecha, hora, sede y documentos necesarios para asistir.",
        "Si no encuentras disponibilidad o tienes dificultades para agendar, solicita orientación a Compensar EPS o a tu IPS."
    ],
    "url_oficial": "https://corporativo.compensar.com/salud/compensar-eps/cita-medica"
    },
    {
    "eps": "Compensar",
    "codigo": "renovar-formula",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Fórmula médica anterior o vigente.",
        "Información de los medicamentos prescritos y del tratamiento.",
        "Comprobante de dispensación o autorización anterior, si está disponible.",
        "Historia clínica o soportes médicos, cuando sean requeridos."
    ],
    "pasos": [
        "Revisa la fecha de expedición y vigencia de tu fórmula médica.",
        "Verifica si tienes entregas pendientes de medicamentos.",
        "Si la fórmula está vigente y tienes entregas pendientes, consulta con el operador farmacéutico asignado cómo solicitar la siguiente entrega.",
        "Si la fórmula está vencida, comunícate con tu IPS o con Compensar EPS para consultar el procedimiento de renovación correspondiente.",
        "Ingresa al portal oficial de Compensar EPS y consulta los canales disponibles para citas médicas y gestión de medicamentos.",
        "Si necesitas una nueva valoración médica, presenta la fórmula anterior y la información de los medicamentos que utilizas.",
        "Cuando el profesional de salud emita una nueva fórmula, verifica si los medicamentos requieren autorización o direccionamiento.",
        "Consulta cuál es el punto de dispensación asignado para reclamar los medicamentos.",
        "Presenta los documentos solicitados y conserva los comprobantes de entrega.",
        "Si tienes dificultades para recibir los medicamentos o continuar el tratamiento, solicita orientación a Compensar EPS mediante sus canales oficiales."
    ],
    "url_oficial": "https://corporativo.compensar.com/salud/plan-de-beneficios-en-salud/compensar-eps/ruta-de-servicios"
    },
    {
    "eps": "Compensar",
    "codigo": "vencimiento-examen",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Orden médica anterior del examen, procedimiento o cirugía.",
        "Autorización anterior, si fue emitida.",
        "Fecha de expedición y vencimiento de los documentos.",
        "Historia clínica y soportes médicos, cuando sean requeridos."
    ],
    "pasos": [
        "Identifica si venció la orden médica o la autorización del servicio.",
        "Revisa las fechas de expedición y vigencia indicadas en los documentos.",
        "Comunícate con la IPS donde se realizará el examen, procedimiento o cirugía para verificar si los documentos todavía pueden utilizarse.",
        "Si venció la orden médica, consulta con tu IPS si necesitas una nueva valoración médica para obtener una orden actualizada.",
        "Si venció la autorización, consulta con la IPS si puede gestionar su actualización directamente ante Compensar EPS.",
        "Si necesitas realizar el trámite personalmente, ingresa a la Ruta de Servicios oficial de Compensar EPS.",
        "Busca la sección de autorizaciones y consulta los canales disponibles para gestionar tu solicitud.",
        "Ten disponibles la orden anterior, la autorización y los soportes clínicos relacionados.",
        "Si el procedimiento ya estaba programado, confirma con la IPS si debes actualizar algún documento antes de asistir.",
        "Cuando tengas los documentos válidos, según corresponda, continúa con la programación del servicio.",
        "Si tienes dificultades para gestionar el trámite, solicita orientación a Compensar EPS o a tu IPS."
    ],
    "url_oficial": "https://corporativo.compensar.com/salud/plan-de-beneficios-en-salud/compensar-eps/ruta-de-servicios"
    },
    {
    "eps": "Compensar",
    "codigo": "vencimiento-especialista",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Orden médica o remisión anterior para valoración con especialista.",
        "Autorización o direccionamiento anterior, si fue emitido.",
        "Fecha de expedición y vencimiento de los documentos.",
        "Historia clínica y soportes médicos, cuando sean requeridos."
    ],
    "pasos": [
        "Revisa la remisión médica y verifica su fecha de expedición y vigencia.",
        "Identifica si venció la remisión médica o la autorización o direccionamiento del servicio.",
        "Consulta con tu IPS si la remisión todavía puede utilizarse para solicitar la cita.",
        "Si la remisión está vencida, pregunta a tu IPS si necesitas una nueva valoración médica.",
        "Si venció la autorización o el direccionamiento, consulta con la IPS si puede gestionar su actualización directamente ante Compensar EPS.",
        "Si necesitas realizar el trámite personalmente, ingresa a la Ruta de Servicios oficial de Compensar EPS.",
        "Busca la sección de autorizaciones y consulta los canales disponibles para gestionar tu solicitud.",
        "Ten disponibles la remisión anterior, la autorización y los soportes médicos relacionados.",
        "Si ya tenías una cita programada, comunícate con la IPS para verificar si necesitas actualizar algún documento.",
        "Cuando tengas los documentos válidos, según corresponda, confirma con la IPS cómo solicitar o mantener la cita con el especialista.",
        "Si tienes dificultades para continuar el trámite, solicita orientación a Compensar EPS o a tu IPS."
    ],
    "url_oficial": "https://corporativo.compensar.com/salud/plan-de-beneficios-en-salud/compensar-eps/ruta-de-servicios"
    },
    {
    "eps": "Famisanar",
    "codigo": "autorizacion-examen",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Orden médica del examen, procedimiento o cirugía.",
        "Historia clínica y soportes médicos, cuando sean requeridos.",
        "Datos de contacto actualizados: teléfono, dirección y correo electrónico.",
        "Correo electrónico o acceso a la Oficina Virtual para recibir la respuesta."
    ],
    "pasos": [
        "Revisa la orden médica e identifica el examen, procedimiento o cirugía solicitado.",
        "Consulta con la IPS si el servicio requiere autorización o si puede gestionarlo directamente.",
        "Si debes solicitar la autorización, ingresa a la página oficial de autorizaciones médicas PBS de Famisanar.",
        "Puedes utilizar la Oficina Virtual, registrarte o iniciar sesión y buscar la opción de autorizaciones.",
        "Carga una imagen o archivo legible de la orden médica y los soportes que solicite el sistema.",
        "Como alternativa, envía la solicitud al correo autorizacionesambulatorias@famisanar.com.co.",
        "En el correo incluye el nombre completo del paciente, documento de identidad, teléfonos, dirección y correo electrónico de respuesta.",
        "Adjunta la orden médica y la historia clínica cuando corresponda. Envía un correo separado por cada paciente.",
        "Conserva el correo enviado o el comprobante de radicación y revisa la respuesta de Famisanar.",
        "Una vez recibida la autorización, verifica el prestador asignado y su vigencia.",
        "Comunícate con la IPS o el profesional indicado para programar el examen, procedimiento o cirugía.",
        "Si tienes dificultades, consulta los canales de atención publicados en la página oficial de Famisanar."
    ],
    "url_oficial": "https://www.famisanar.com.co/afiliados/pbs/autorizaciones-medicas"
    },
    {
    "eps": "Famisanar",
    "codigo": "autorizacion-especialista",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Orden médica o remisión para valoración con especialista.",
        "Historia clínica y soportes médicos, cuando sean requeridos.",
        "Datos de contacto actualizados: teléfono y correo electrónico.",
        "Acceso a la Oficina Virtual o al canal de atención habilitado para autorizaciones."
    ],
    "pasos": [
        "Revisa la orden médica e identifica la especialidad solicitada.",
        "Consulta con tu IPS si la remisión requiere autorización o si la institución realiza directamente la gestión.",
        "Verifica si ya existe un direccionamiento hacia una IPS especializada.",
        "Si debes solicitar una autorización, ingresa a la página oficial de autorizaciones médicas PBS de Famisanar.",
        "Consulta las opciones de la Oficina Virtual y los canales habilitados para presentar solicitudes.",
        "Si el canal permite radicar tu solicitud, proporciona los datos del paciente y adjunta la remisión médica y los soportes requeridos.",
        "Si utilizas un canal de correo electrónico publicado por Famisanar, verifica primero que corresponda a tu tipo de solicitud.",
        "Conserva el comprobante o número de radicado, si se genera.",
        "Consulta el estado de la solicitud mediante los canales oficiales de Famisanar.",
        "Cuando recibas la autorización o el direccionamiento, verifica cuál es la IPS asignada.",
        "Comunícate con la IPS indicada para solicitar la cita con el especialista.",
        "Si tienes dificultades para obtener la autorización o la cita, solicita orientación a Famisanar o a tu IPS."
    ],
    "url_oficial": "https://www.famisanar.com.co/afiliados/pbs/autorizaciones-medicas"
    },
    {
    "eps": "Famisanar",
    "codigo": "asignacion-cita",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Estar afiliado a Famisanar EPS.",
        "Conocer la IPS primaria asignada.",
        "Tener actualizados los datos de contacto.",
        "Contar con una remisión o autorización si se solicita una consulta especializada que la requiera."
    ],
    "pasos": [
        "Identifica la IPS primaria que tienes asignada en Famisanar.",
        "Verifica si necesitas una cita de medicina general o una consulta especializada.",
        "Para medicina general, consulta los canales de asignación de citas de tu IPS primaria.",
        "Ingresa al portal oficial de Famisanar y busca la información sobre su red de atención y servicios para afiliados.",
        "Verifica si tu IPS permite solicitar citas por teléfono, internet o atención presencial.",
        "Selecciona el canal habilitado y proporciona los datos necesarios para solicitar la cita.",
        "Si necesitas una consulta con especialista, verifica previamente si debes gestionar una remisión o autorización.",
        "Confirma la fecha, hora, sede y documentos necesarios para asistir.",
        "Si no encuentras disponibilidad o tienes dificultades para agendar, solicita orientación a tu IPS o a Famisanar."
    ],
    "url_oficial": "https://www.famisanar.com.co/"
    },
    {
    "eps": "Famisanar",
    "codigo": "renovar-formula",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Fórmula médica anterior o vigente.",
        "Información de los medicamentos prescritos y del tratamiento.",
        "Comprobante de dispensación o autorización anterior, si está disponible.",
        "Historia clínica o soportes médicos, cuando sean requeridos."
    ],
    "pasos": [
        "Revisa la fecha de expedición y vigencia de tu fórmula médica.",
        "Verifica si tienes entregas pendientes de medicamentos.",
        "Si la fórmula está vigente y tienes entregas pendientes, consulta con el operador farmacéutico asignado por Famisanar cómo solicitar la siguiente entrega.",
        "Si la fórmula está vencida, comunícate con tu IPS primaria para consultar si necesitas una nueva valoración médica.",
        "Ingresa al portal oficial de Famisanar para consultar los canales de atención y gestión de medicamentos.",
        "Si necesitas una nueva valoración, presenta la fórmula anterior y la información de los medicamentos que utilizas.",
        "Cuando el profesional de salud emita una nueva fórmula, verifica si los medicamentos requieren autorización o direccionamiento.",
        "Consulta cuál es el punto de dispensación asignado para reclamar los medicamentos.",
        "Presenta los documentos solicitados y conserva los comprobantes de entrega.",
        "Si tienes dificultades para acceder a los medicamentos o continuar el tratamiento, solicita orientación a Famisanar o a tu IPS."
    ],
    "url_oficial": "https://www.famisanar.com.co/"
    },
    {
    "eps": "Famisanar",
    "codigo": "vencimiento-examen",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Orden médica anterior del examen, procedimiento o cirugía.",
        "Autorización anterior, si fue emitida.",
        "Fecha de expedición y vencimiento de los documentos.",
        "Historia clínica y soportes médicos, cuando sean requeridos."
    ],
    "pasos": [
        "Identifica si venció la orden médica o la autorización del servicio.",
        "Revisa las fechas de expedición y vigencia indicadas en los documentos.",
        "Comunícate con la IPS donde se realizará el examen, procedimiento o cirugía para verificar si los documentos todavía pueden utilizarse.",
        "Si venció la orden médica, consulta con tu IPS si necesitas una nueva valoración médica para obtener una orden actualizada.",
        "Si venció la autorización, consulta con la IPS si puede gestionar su actualización directamente ante Famisanar.",
        "Si necesitas realizar una solicitud personalmente, ingresa a la página oficial de autorizaciones médicas PBS de Famisanar.",
        "Consulta los canales disponibles para presentar una solicitud de autorización o actualización.",
        "Ten disponibles la orden anterior, la autorización y los soportes clínicos relacionados.",
        "Conserva el número de radicado o comprobante, si el sistema lo genera.",
        "Si el procedimiento ya estaba programado, confirma con la IPS si debes actualizar algún documento antes de asistir.",
        "Cuando tengas los documentos válidos, según corresponda, continúa con la programación del servicio.",
        "Si tienes dificultades para gestionar el trámite, solicita orientación a Famisanar o a tu IPS."
    ],
    "url_oficial": "https://www.famisanar.com.co/afiliados/pbs/autorizaciones-medicas"
    },
    {
    "eps": "Famisanar",
    "codigo": "vencimiento-especialista",
    "requisitos": [
        "Documento de identidad del paciente.",
        "Orden médica o remisión anterior para valoración con especialista.",
        "Autorización o direccionamiento anterior, si fue emitido.",
        "Fecha de expedición y vencimiento de los documentos.",
        "Historia clínica y soportes médicos, cuando sean requeridos."
    ],
    "pasos": [
        "Revisa la remisión médica y verifica su fecha de expedición y vigencia.",
        "Identifica si venció la remisión médica o la autorización o direccionamiento del servicio.",
        "Consulta con tu IPS si la remisión todavía puede utilizarse para solicitar la cita.",
        "Si la remisión está vencida, pregunta a tu IPS si necesitas una nueva valoración médica para obtener una orden actualizada.",
        "Si venció la autorización o el direccionamiento, consulta con la IPS si puede gestionar su actualización directamente ante Famisanar.",
        "Si necesitas realizar el trámite personalmente, ingresa a la página oficial de autorizaciones médicas PBS de Famisanar.",
        "Consulta los canales disponibles para presentar una solicitud o actualizar una autorización.",
        "Ten disponibles la remisión anterior, la autorización y los soportes médicos relacionados.",
        "Conserva el número de radicado o comprobante, si se genera.",
        "Si ya tenías una cita programada, comunícate con la IPS para verificar si necesitas actualizar algún documento.",
        "Cuando tengas los documentos válidos, según corresponda, confirma con la IPS cómo solicitar o mantener la cita con el especialista.",
        "Si tienes dificultades para continuar el trámite, solicita orientación a Famisanar o a tu IPS."
    ],
    "url_oficial": "https://www.famisanar.com.co/afiliados/pbs/autorizaciones-medicas"
}

]


with app.app_context():
    for item in orientaciones:
        eps = EPS.query.filter_by(name=item["eps"]).first()
        tramite = Tramite.query.filter_by(code=item["codigo"]).first()

        if not eps or not tramite:
            print(f"No encontrado: {item['eps']} - {item['codigo']}")
            continue

        registro = EPSTramite.query.filter_by(
            eps_id=eps.id,
            tramite_id=tramite.id
        ).first()

        if registro is None:
            registro = EPSTramite(
                eps_id=eps.id,
                tramite_id=tramite.id
            )
            db.session.add(registro)

        registro.requisitos = item["requisitos"]
        registro.pasos = item["pasos"]
        registro.url_oficial = item["url_oficial"]
        registro.fecha_verificacion = None
        registro.is_active = True

    db.session.commit()
    print("Orientaciones cargadas correctamente.")