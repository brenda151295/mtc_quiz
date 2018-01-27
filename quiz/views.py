
from random import shuffle

from django.shortcuts import render, get_object_or_404

from quiz.models import Pregunta
from quiz import constants


def home(request):
    context = {'latest_question_list': None}

    return render(request, 'home.html', context)


def levels(request):
    context = {'categoria': request.GET.get('categoria', 'AI')}

    return render(request, 'levels.html', context)


def get_preguntas(categoria):
    var = 'categoria_' + categoria
    params = {
        var: True
    }
    preguntas = list(Pregunta.objects.filter(**params))
    shuffle(preguntas)
    for i in preguntas:
        # yield
        yield i


def pregunta_siguiente(funcion):

    def wrapper(*args):
        generator = constants.GENERATORS.get(args[0], None)
        if generator is None:
            constants.GENERATORS[args[0]] = get_preguntas(args[0])
        return funcion(*args)

    return wrapper


@pregunta_siguiente
def pregunta_random(categoria):
    generator = constants.GENERATORS.get(categoria)
    try:
        return next(generator)
    except:
        return None


def basico(request):
    if request.method == 'GET':
        categoria = request.GET.get('categoria', 'AI')
        pregunta = pregunta_random(categoria)
        context = {
            'categoria': categoria,
            'pregunta': pregunta
        }
    else:
        siguiente = request.POST.get('siguiente', None)
        categoria = request.POST.get('categoria', 'AI')
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
    if request.method == 'GET':            
        pregunta = Pregunta.objects.first()
        context = {
            'categoria': request.GET.get('categoria', 'AI'),
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
                'categoria': request.GET.get('categoria', 'AI'),
                'pregunta': pregunta,
                'respondida': True,
                'alternativa_seleccionada':alternativa_seleccionada,
            }
        else:
            pregunta = Pregunta.objects.last()
            context = {
                'categoria': request.GET.get('categoria', 'AI'),
                'pregunta': pregunta,
                'respondida': False
            }

    return render(request, 'intermedio.html', context)



def avanzado(request):
    context = {'categoria': request.GET.get('categoria', 'AI')}
    return render(request, 'basico.html', context)
