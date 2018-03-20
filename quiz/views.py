
from random import shuffle
from datetime import datetime
from datetime import timedelta


from django.shortcuts import render, get_object_or_404

from quiz.models import Pregunta
from quiz import constants


def home(request):
    context = {'latest_question_list': None}

    return render(request, 'home.html', context)


def levels(request):
    context = {'categoria': request.GET.get('categoria', 'AI')}

    return render(request, 'levels.html', context)


def get_preguntas(categoria, limite = None):
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
        if len(args) == 1:
            limite = None
        else:
            limite = args[1]

        generator = constants.GENERATORS.get(args[0], None)
        if generator is None:
            constants.GENERATORS[args[0]] = get_preguntas(args[0], limite)
        return funcion(*args)

    return wrapper  

def resetear_generator(categoria, limite=None):
    constants.GENERATORS[categoria] = get_preguntas(categoria, limite)

def resetear_examen():
    constants.EXAMEN = []

def guardar_pregunta(pregunta, alternativa_correcta, alternativa_seleccionada):
    constants.EXAMEN.append([pregunta, alternativa_correcta, alternativa_seleccionada])

@pregunta_siguiente
def pregunta_random(categoria, limite=None):
    generator = constants.GENERATORS.get(categoria)
    try:
        return next(generator)
    except:
        resetear_generator(categoria)
        return None

        

def basico(request):
    print ("-------------------------------")
    print (request.GET)
    print (request.POST)
    print ("-------------------------------")
    categoria = request.GET.get('categoria', 'AI')
    if request.method == 'GET':
        resetear_generator(categoria)
        resetear_examen()
        pregunta = pregunta_random(categoria)
        context = {
            'numero': len(constants.EXAMEN)+1,
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
                guardar_pregunta(pregunta, alternativa_correcta, alternativa_seleccionada)
            context = {
                'numero': len(constants.EXAMEN)+1 if not es_correcta else len(constants.EXAMEN),
                'es_correcta': es_correcta,
                'alternativa_correcta': alternativa_correcta,
                'categoria': categoria,
                'pregunta': pregunta
            }
        else:
            pregunta = pregunta_random(categoria)
            if pregunta is None:
                return render(request, 'estadisticas.html')
            context = { 
                'numero': len(constants.EXAMEN)+1,
                'categoria': categoria,
                'pregunta': pregunta
            }

    return render(request, 'basico.html', context)


def obtener_puntaje():
    num_correctas = 0
    num_incorrectas = 0
    for pregunta, alternativa_correcta, alternativa_seleccionada in constants.EXAMEN:
        if alternativa_correcta == alternativa_seleccionada:
            num_correctas += 1
        else:
            num_incorrectas += 1
    return (num_correctas, num_incorrectas)


def intermedio(request):
    categoria = request.GET.get('categoria', 'AI')
    if request.method == 'GET':
        resetear_generator(categoria, constants.NUM_PREGUNTAS) 
        resetear_examen()  
        pregunta = pregunta_random(categoria, constants.NUM_PREGUNTAS)
        context = {
            'numero': len(constants.EXAMEN)+1,
            'categoria': categoria,
            'pregunta': pregunta
        }
    else:
        siguiente = request.POST.get('siguiente', None)
        if siguiente is None:
            id_pregunta = request.POST.get('id')
            alternativa_seleccionada = request.POST.get('alternativa')
            pregunta = get_object_or_404(Pregunta, pk=id_pregunta)
            alternativa_correcta = constants.ALTERNATIVA_CORRECTA.get(pregunta.alternativa_correcta)
            es_correcta = alternativa_correcta == alternativa_seleccionada
            guardar_pregunta(pregunta, alternativa_correcta, alternativa_seleccionada)
            context = {
                'numero': len(constants.EXAMEN),
                'es_correcta' : es_correcta,
                'alternativa_correcta' : alternativa_correcta,
                'alternativa_correcta_letra' : pregunta.alternativa_correcta,
                'categoria': categoria,
                'pregunta': pregunta,
                'respondida': True,
                'alternativa_seleccionada':alternativa_seleccionada,
            }   
        else:
            pregunta = pregunta_random(categoria, constants.NUM_PREGUNTAS)
            puntaje_correcto, puntaje_incorrecto = obtener_puntaje()
            aprobar = puntaje_correcto >= constants.NUM_PREGUNTAS_APROBAR
            if pregunta is None:
                context = {
                    'examen': enumerate(constants.EXAMEN,1),
                    'puntaje_correcto': puntaje_correcto,
                    'puntaje_incorrecto': puntaje_incorrecto,
                    'total_preguntas': constants.NUM_PREGUNTAS,
                    'preguntas_respondidas': len(constants.EXAMEN),
                    'preguntas_no_respondidas': constants.NUM_PREGUNTAS - len(constants.EXAMEN),
                    'aprobo': aprobar
                }
                return render(request, 'estadisticas.html', context)
            context = {
                'numero': len(constants.EXAMEN)+1,
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


def obtener_tiempo():
    return constants.TIEMPO_EXAMEN.isoformat()      


def avanzado(request):
    
    #Fixme: cuando se caba el tiempo no da resultados

    categoria = request.GET.get('categoria', 'AI')
    if request.method == 'GET':
        resetear_generator(categoria, constants.NUM_PREGUNTAS) 
        resetear_examen() 
        constants.TIEMPO_EXAMEN = datetime.now() + timedelta(seconds = 100)
        pregunta = pregunta_random(categoria, constants.NUM_PREGUNTAS)
        context = {
            'numero': len(constants.EXAMEN)+1,
            'categoria': categoria,
            'pregunta': pregunta,
            'tiempo': obtener_tiempo()
        }
    else:
        id_pregunta = request.POST.get('id')
        alternativa_seleccionada = request.POST.get('alternativa')
        pregunta = get_object_or_404(Pregunta, pk=id_pregunta)
        alternativa_correcta = constants.ALTERNATIVA_CORRECTA.get(pregunta.alternativa_correcta)
        es_correcta = alternativa_correcta == alternativa_seleccionada
        guardar_pregunta(pregunta, alternativa_correcta, alternativa_seleccionada)
        
        pregunta = pregunta_random(categoria, constants.NUM_PREGUNTAS)

        context = {
            'numero': len(constants.EXAMEN)+1,
            'categoria': categoria,
            'pregunta': pregunta,
            'respondida': False,
            'tiempo': obtener_tiempo()
        }
        if len (constants.EXAMEN) == constants.NUM_PREGUNTAS:
            puntaje_correcto, puntaje_incorrecto = obtener_puntaje()
            aprobar = puntaje_correcto >= constants.NUM_PREGUNTAS_APROBAR
            context = {
                'examen': enumerate(constants.EXAMEN,1),
                'puntaje_correcto': puntaje_correcto,
                'puntaje_incorrecto': puntaje_incorrecto,
                'total_preguntas': constants.NUM_PREGUNTAS,
                'preguntas_respondidas': len(constants.EXAMEN),
                'preguntas_no_respondidas': constants.NUM_PREGUNTAS - len(constants.EXAMEN),
                'aprobo': aprobar
            }
            return render(request, 'estadisticas.html', context)        

    return render(request, 'avanzado.html', context)


def estadisticas(request):
    puntaje_correcto, puntaje_incorrecto = obtener_puntaje()
    aprobar = puntaje_correcto >= constants.NUM_PREGUNTAS_APROBAR
    context = {
        'examen': enumerate(constants.EXAMEN,1),
        'puntaje_correcto': puntaje_correcto,
        'puntaje_incorrecto': puntaje_incorrecto,
        'total_preguntas': constants.NUM_PREGUNTAS,
        'preguntas_respondidas': len(constants.EXAMEN),
        'preguntas_no_respondidas': constants.NUM_PREGUNTAS - len(constants.EXAMEN),
        'aprobo': aprobar
    }
    return render(request, 'estadisticas.html', context)