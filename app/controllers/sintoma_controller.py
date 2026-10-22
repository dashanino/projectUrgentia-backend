from flask import jsonify
from app.services.sintoma_service import sintoma_redflag_service


def sintoma_redflag_controller(id_bandera):

    try:
        sintomas = sintoma_redflag_service(id_bandera)

        return jsonify({
            'ok': True,
            'sintomas': sintomas
        }), 200

    except Exception as e:
        return jsonify({
            'ok': False,
            'mensaje': 'Error al obtener los síntomas',
            'error': str(e)
        }), 500