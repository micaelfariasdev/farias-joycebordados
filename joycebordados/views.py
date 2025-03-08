from django.shortcuts import render
from empresa.models import Empresa


def HomeView(request):
    dados = Empresa.objects.get(pk=1)
    fotos = dados.fotos_carrossel.all() if dados else []
    return render(request, 'joycebordados/index.html', context={'dados': dados, 'fotos': fotos,})
