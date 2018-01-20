from django.shortcuts import render


def home(request):
    context = {'latest_question_list': None}
    return render(request, 'home.html', context)

def levels(request):
    context = {'latest_question_list': None}
    return render(request, 'levels.html', context)