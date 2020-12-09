from django.shortcuts import render


def index(request):
    context = {
        'app_name': 'Foods'
    }
    return render(request, 'index.html', context)
