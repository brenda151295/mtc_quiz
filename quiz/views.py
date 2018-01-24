from django.shortcuts import render, get_object_or_404
from quiz.models import Pregunta
from quiz import constants

def home(request):
    context = {'latest_question_list': None}

    return render(request, 'home.html', context)


def levels(request):
    context = {'categoria': request.GET.get('categoria', 'AI')}
    print(context)

    return render(request, 'levels.html', context)

def basico(request):
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
                'categoria': request.GET.get('categoria', 'AI'),
                'pregunta': pregunta   
            }
        else:
            pregunta = Pregunta.objects.last()
            context = {
                'categoria': request.GET.get('categoria', 'AI'),
                'pregunta': pregunta
            }

    return render(request, 'basico.html', context)

def intermedio(request):
    context = {'categoria': request.GET.get('categoria', 'AI')}
    return render(request, 'basico.html', context)

def avanzado(request):
    context = {'categoria': request.GET.get('categoria', 'AI')}
    return render(request, 'basico.html', context)