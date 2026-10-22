from app import create_app
from app.extensions import db
from app.models.sintoma import Sintoma

app = create_app()

sintomas = [
    # Dolor de cabeza (id_red_flag = 2)
    {
        'id_bandera': 2,
        'name': 'Dolor apareció de manera súbita y muy intensa'
    },
    {
        'id_bandera': 2,
        'name': 'Peor dolor de cabeza de la vida'
    },
    {
        'id_bandera': 2,
        'name': 'Rigidez en el cuello'
    },
    {
        'id_bandera': 2,
        'name': 'Pérdida de conciencia o desmayo'
    },
    {
        'id_bandera': 2,
        'name': 'Visión borrosa o dificultad para hablar'
    },
    {
        'id_bandera': 2,
        'name': 'Golpe en la cabeza'
    },

    # Dolor de abdomen (id_red_flag = 4)
    {
        'id_bandera': 4,
        'name': 'Dolor muy intenso sin mejora'
    },
    {
        'id_bandera': 4,
        'name': 'Abdomen muy duro o sensible'
    },
    {
        'id_bandera': 4,
        'name': 'Vómito constante'
    },
    {
        'id_bandera': 4,
        'name': 'Sangre en vómito o heces'
    },


    # Fiebre (id_red_flag = 6)
    {
        'id_bandera': 6,
        'name': 'Fiebre mayor a 39 °C'
    },
    {
        'id_bandera': 6,
        'name': 'Somnolencia o confusión'
    },
    {
        'id_bandera': 6,
        'name': 'Rigidez en el cuello'
    },
    {
        'id_bandera': 6,
        'name': 'Manchas en la piel'
    },

    # Caída o golpe reciente (id_red_flag = 7)
    {
        'id_bandera': 7,
        'name': 'Pérdida de conciencia o desmayo después del golpe'
    },
    {
        'id_bandera': 7,
        'name': 'Confusión, desorientación o comportamiento diferente'
    },
    {
        'id_bandera': 7,
        'name': 'Somnolencia inusual o dificultad para mantenerse despierto'
    },
    {
        'id_bandera': 7,
        'name': 'Vómitos después del golpe'
    },
    {
        'id_bandera': 7,
        'name': 'Debilidad o dificultad para mover un brazo o una pierna'
    },
    {
        'id_bandera': 7,
        'name': 'Dificultad para hablar o entender'
    },
    {
        'id_bandera': 7,
        'name': 'Sangrado o salida de líquido por la nariz o los oídos'
    },
    #tos con sangre id_bandera:9
    {
        'id_bandera': 9,
        'name': 'Cantidad de sangre considerable o abundante'
    },
    
    {
        'id_bandera': 9,
        'name': 'Mareo, debilidad o sensación de desmayo'
    },
    # posible fractura o deformidad: id_bandera:17
    {
        'id_bandera': 17,
        'name': 'Dolor intenso en la zona afectada'
    },
    {
        'id_bandera': 17,
        'name': 'Hinchazón importante'
    },
    {
        'id_bandera': 17,
        'name': 'Incapacidad para mover la zona afectada'
    },
    {
        'id_bandera': 17,
        'name': 'Entumecimiento u hormigueo'
    },
    {
        'id_bandera': 17,
        'name': 'La extremidad está fría, pálida o azulada'
    },
    {
        'id_bandera': 17,
        'name': 'Herida abierta en la zona de la lesión'
    },
]


with app.app_context():
    for item in sintomas:

        sintoma = Sintoma.query.filter_by(
            id_bandera=item['id_bandera'],
            name=item['name']
        ).first()

        if sintoma:
            continue

        db.session.add(
            Sintoma(
                id_bandera=item['id_bandera'],
                name=item['name']
            )
        )

    db.session.commit()