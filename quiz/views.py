
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

def resetear_generator(categoria):
    constants.GENERATORS[categoria] = get_preguntas(categoria)

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
        pregunta = pregunta_random(categoria)
        context = {
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
            context = {
                'es_correcta': es_correcta,
                'alternativa_correcta': alternativa_correcta,
                'categoria': categoria,
                'pregunta': pregunta
            }
        else:
            pregunta = pregunta_random(categoria)
            context = { 
                'categoria': categoria,
                'pregunta': pregunta
            }

    return render(request, 'basico.html', context)


def intermedio(request):
    categoria = request.GET.get('categoria', 'AI')
    if request.method == 'GET':
        resetear_generator(categoria)  
        pregunta = pregunta_random(categoria)
        context = {
            'categoria': categoria,
            'pregunta': pregunta
        }
    else:
        siguiente = request.POST.get('siguiente', None)
        if siguiente == None:
            id_pregunta = request.POST.get('id')
            alternativa_seleccionada = request.POST.get('alternativa')
            pregunta = get_object_or_404(Pregunta, pk=id_pregunta)
            alternativa_correcta = constants.ALTERNATIVA_CORRECTA.get(pregunta.alternativa_correcta)
            es_correcta = alternativa_correcta == alternativa_seleccionada
            context = {
                'es_correcta' : es_correcta,
                'alternativa_correcta' : alternativa_correcta,
                'alternativa_correcta_letra' : pregunta.alternativa_correcta,
                'categoria': categoria,
                'pregunta': pregunta,
                'respondida': True,
                'alternativa_seleccionada':alternativa_seleccionada,
            }
        else:
            pregunta = pregunta_random(categoria)
            context = {
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
    limite = 4
    categoria = request.GET.get('categoria', 'AI')
    if request.method == 'GET':
        resetear_generator(categoria) 
        resetear_examen() 
        constants.TIEMPO_EXAMEN = datetime.now() + timedelta(minutes=40)
        pregunta = pregunta_random(categoria, limite)
        context = {
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
        
        pregunta = pregunta_random(categoria, limite)

        context = {
            'categoria': categoria,
            'pregunta': pregunta,
            'respondida': False,
            'tiempo': obtener_tiempo()
        }
        if len (constants.EXAMEN) == limite:
            return render(request, 'estadisticas.html', context)            

    return render(request, 'avanzado.html', context)

def estadisticas(request):
    return render(request, 'estadisticas.html')