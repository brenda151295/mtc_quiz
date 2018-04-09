from random import getrandbits, shuffle
from datetime import datetime
from datetime import timedelta
from collections import Counter

import pytz

from django.shortcuts import render, get_object_or_404

from quiz.models import Pregunta
from quiz import constants


def reset_session_data(hash_id):
    constants.SESSION_DATA[hash_id] = {
        'EXAMEN': [],
        'EXAMEN_DATA': {},
        'GENERATORS': {},
        'TIEMPO_EXAMEN': None
    }


def get_hash(request, force_reset=False):
    hash_id = request.session.get('hash_id', None)
    if hash_id is None:
        hash_id = str(getrandbits(128))
        request.session['hash_id'] = hash_id
        reset_session_data(hash_id)
    elif constants.SESSION_DATA.get(hash_id, None) is None or force_reset:
        reset_session_data(hash_id)

    return hash_id


def home(request):
    context = {'latest_question_list': None}

    return render(request, 'home.html', context)


def levels(request):
    context = {'categoria': request.GET.get('categoria', 'AI')}

    return render(request, 'levels.html', context)


def get_preguntas(categoria, limite=None):
    var = 'categoria_' + categoria
    params = {
        var: True
    }
    preguntas = list(Pregunta.objects.filter(**params))
    shuffle(preguntas)
    if limite is not None:
        preguntas = preguntas[:limite]

    for i in preguntas:
        # yield
        yield i


def pregunta_siguiente(funcion):

    def wrapper(*args):
        if len(args) == 2:
            limite = None
        else:
            limite = args[2]

        request = args[0]
        get_session_data(request)['GENERATORS']
        generator = get_session_data(request)['GENERATORS'].get(args[1], None)
        if generator is None:
            get_session_data(request)['GENERATORS'][args[1]] = get_preguntas(
                args[1], limite)
        return funcion(*args)

    return wrapper


def resetear_generator(request, categoria, limite=None):
    get_session_data(request)['GENERATORS'][categoria] = (
        get_preguntas(categoria, limite)
    )


def resetear(request):
    get_hash(request, force_reset=True)


def get_session_data(request):
    hash_id = get_hash(request)
    return constants.SESSION_DATA[hash_id]


def guardar_pregunta(request, pregunta, alternativa_correcta, alternativa_seleccionada):

    get_session_data(request)['EXAMEN'].append(
        [pregunta, alternativa_correcta, alternativa_seleccionada])


@pregunta_siguiente
def pregunta_random(request, categoria, limite=None):
    generator = get_session_data(request)['GENERATORS'].get(categoria)
    try:
        return next(generator)
    except:
        resetear_generator(request, categoria)
        return None


def guardar_data(request, id_pregunta):
    counter = get_session_data(request)['EXAMEN_DATA'].get(id_pregunta, 0)
    get_session_data(request)['EXAMEN_DATA'][id_pregunta] = counter + 1


def basico(request):
    categoria = request.GET.get('categoria', 'AI')
    if request.method == 'GET':
        resetear_generator(request, categoria)
        resetear(request)
        pregunta = pregunta_random(request, categoria)

        context = {
            'numero': len(get_session_data(request)['EXAMEN']) + 1,
            'categoria': categoria,
            'pregunta': pregunta
        }
    else:
        siguiente = request.POST.get('siguiente', None)
        if siguiente is None:
            id_pregunta = request.POST.get('id')
            alternativa_seleccionada = request.POST.get('alternativa')
            pregunta = get_object_or_404(Pregunta, pk=id_pregunta)
            alternativa_correcta = constants.ALTERNATIVA_CORRECTA.get(
                pregunta.alternativa_correcta)
            es_correcta = alternativa_correcta == alternativa_seleccionada
            if es_correcta:
                guardar_pregunta(
                    request, pregunta, alternativa_correcta, alternativa_seleccionada)
            guardar_data(request, id_pregunta)
            context = {
                'numero': (
                    len(get_session_data(request)['EXAMEN']) + 1
                    if not es_correcta
                    else len(get_session_data(request)['EXAMEN'])),
                'es_correcta': es_correcta,
                'alternativa_correcta': alternativa_correcta,
                'categoria': categoria,
                'pregunta': pregunta
            }
        else:
            pregunta = pregunta_random(request, categoria)
            context = {
                'numero': len(get_session_data(request)['EXAMEN']) + 1,
                'categoria': categoria,
                'pregunta': pregunta
            }
            if pregunta is None:
                context['intentos'] = dict(
                    Counter(get_session_data(request)['EXAMEN_DATA'].values()))
                get_session_data(request)['EXAMEN_DATA'] = {}
                return render(request, 'estadisticas_basico.html', context)

    return render(request, 'basico.html', context)


def obtener_puntaje(request):
    num_correctas = 0
    num_incorrectas = 0
    for pregunta, alternativa_correcta, alternativa_seleccionada in get_session_data(request)['EXAMEN']:
        if alternativa_correcta == alternativa_seleccionada:
            num_correctas += 1
        else:
            num_incorrectas += 1
    return (num_correctas, num_incorrectas)


def intermedio(request):
    categoria = request.GET.get('categoria', 'AI')
    if request.method == 'GET':
        resetear_generator(request, categoria, constants.NUM_PREGUNTAS)
        resetear(request)
        pregunta = pregunta_random(request, categoria, constants.NUM_PREGUNTAS)
        context = {
            'numero': len(get_session_data(request)['EXAMEN']) + 1,
            'categoria': categoria,
            'pregunta': pregunta
        }
    else:
        siguiente = request.POST.get('siguiente', None)
        if siguiente is None:
            id_pregunta = request.POST.get('id')
            alternativa_seleccionada = request.POST.get('alternativa')
            pregunta = get_object_or_404(Pregunta, pk=id_pregunta)
            alternativa_correcta = constants.ALTERNATIVA_CORRECTA.get(
                pregunta.alternativa_correcta)
            es_correcta = alternativa_correcta == alternativa_seleccionada
            guardar_pregunta(
                request, pregunta, alternativa_correcta, alternativa_seleccionada)
            context = {
                'numero': len(get_session_data(request)['EXAMEN']),
                'es_correcta': es_correcta,
                'alternativa_correcta': alternativa_correcta,
                'alternativa_correcta_letra': pregunta.alternativa_correcta,
                'categoria': categoria,
                'pregunta': pregunta,
                'respondida': True,
                'alternativa_seleccionada': alternativa_seleccionada,
            }
        else:
            pregunta = pregunta_random(request, categoria, constants.NUM_PREGUNTAS)
            puntaje_correcto, puntaje_incorrecto = obtener_puntaje(request)
            aprobar = puntaje_correcto >= constants.NUM_PREGUNTAS_APROBAR
            if pregunta is None:
                context = {
                    'examen': enumerate(get_session_data(request)['EXAMEN'], 1),
                    'puntaje_correcto': puntaje_correcto,
                    'puntaje_incorrecto': puntaje_incorrecto,
                    'total_preguntas': constants.NUM_PREGUNTAS,
                    'preguntas_respondidas': len(get_session_data(request)['EXAMEN']),
                    'preguntas_no_respondidas': (
                        constants.NUM_PREGUNTAS - len(get_session_data(request)['EXAMEN'])),
                    'aprobo': aprobar
                }
                return render(request, 'estadisticas.html', context)
            context = {
                'numero': len(get_session_data(request)['EXAMEN']) + 1,
                'categoria': categoria,
                'pregunta': pregunta,
                'respondida': False
            }

    return render(request, 'intermedio.html', context)


def previo_avanzado(request):
    categoria = request.GET.get('categoria', 'AI')
    context = {
        'categoria': categoria,
    }
    return render(request, 'previo_avanzado.html', context)


def reset_tiempo_examen(request):
    get_session_data(request)['TIEMPO_EXAMEN'] = (
        datetime.now(pytz.utc) + timedelta(seconds=2400)
    )


def obtener_tiempo(request):
    tiempo = get_session_data(request)['TIEMPO_EXAMEN']
    if tiempo is None:
        reset_tiempo_examen(request)

    return get_session_data(request)['TIEMPO_EXAMEN'].isoformat()


def avanzado(request):
    # FIXME: cuando se caba el tiempo no da resultados

    categoria = request.GET.get('categoria', 'AI')
    if request.method == 'GET':
        resetear_generator(request, categoria, constants.NUM_PREGUNTAS)
        resetear(request)
        reset_tiempo_examen(request)
        pregunta = pregunta_random(request, categoria, constants.NUM_PREGUNTAS)
        context = {
            'numero': len(get_session_data(request)['EXAMEN']) + 1,
            'categoria': categoria,
            'pregunta': pregunta,
            'tiempo': obtener_tiempo(request)
        }
    else:
        id_pregunta = request.POST.get('id')
        alternativa_seleccionada = request.POST.get('alternativa')
        pregunta = get_object_or_404(Pregunta, pk=id_pregunta)
        alternativa_correcta = constants.ALTERNATIVA_CORRECTA.get(
            pregunta.alternativa_correcta)
        guardar_pregunta(
            request, pregunta, alternativa_correcta, alternativa_seleccionada)

        pregunta = pregunta_random(request, categoria, constants.NUM_PREGUNTAS)

        context = {
            'numero': len(get_session_data(request)['EXAMEN']) + 1,
            'categoria': categoria,
            'pregunta': pregunta,
            'respondida': False,
            'tiempo': obtener_tiempo(request)
        }
        if len(get_session_data(request)['EXAMEN']) == constants.NUM_PREGUNTAS:
            puntaje_correcto, puntaje_incorrecto = obtener_puntaje(request)
            aprobar = puntaje_correcto >= constants.NUM_PREGUNTAS_APROBAR
            context = {
                'examen': enumerate(get_session_data(request)['EXAMEN'], 1),
                'puntaje_correcto': puntaje_correcto,
                'puntaje_incorrecto': puntaje_incorrecto,
                'total_preguntas': constants.NUM_PREGUNTAS,
                'preguntas_respondidas': len(get_session_data(request)['EXAMEN']),
                'preguntas_no_respondidas': (
                    constants.NUM_PREGUNTAS - len(get_session_data(request)['EXAMEN'])),
                'aprobo': aprobar
            }
            return render(request, 'estadisticas.html', context)

    return render(request, 'avanzado.html', context)


def estadisticas(request):
    puntaje_correcto, puntaje_incorrecto = obtener_puntaje(request)
    aprobar = puntaje_correcto >= constants.NUM_PREGUNTAS_APROBAR
    context = {
        'examen': enumerate(get_session_data(request)['EXAMEN'], 1),
        'puntaje_correcto': puntaje_correcto,
        'puntaje_incorrecto': puntaje_incorrecto,
        'total_preguntas': constants.NUM_PREGUNTAS,
        'preguntas_respondidas': len(get_session_data(request)['EXAMEN']),
        'preguntas_no_respondidas': (
            constants.NUM_PREGUNTAS - len(get_session_data(request)['EXAMEN'])),
        'aprobo': aprobar
    }
    return render(request, 'estadisticas.html', context)
