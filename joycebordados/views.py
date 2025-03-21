from django.shortcuts import render, redirect
from empresa.models import Empresa
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def HomeView(request):
    dados = Empresa.objects.get(pk=1)
    fotos = dados.fotos_carrossel.all() if dados else []
    return render(request, 'joycebordados/index.html', context={'dados': dados, 'fotos': fotos, })

def red(request, cod):
    return redirect(f'/cliente/pedido/?codigo={cod}')