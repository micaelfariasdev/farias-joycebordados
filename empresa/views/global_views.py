from django.http import JsonResponse
from django.shortcuts import render, redirect
from ..forms import CustomLoginForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from ..models import Empresa, Pedido
from ..utils import Json_Grafico, enviar_msg, Json_Pedido
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def fechar_pagina(request):
    return render(request, 'global/fechar.html')

def Login(request):
    if request.user.is_authenticated:
        return redirect('adm:empresa')
    dados = Empresa.objects.get(pk=1)
    if request.method == 'POST':
        form = CustomLoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('adm:empresa')
            else:
                form.add_error(None, 'Usuário ou senha inválidos')
        else:
            form.add_error(None, 'Erro no formulário de login')
    else:
        form = CustomLoginForm()

    return render(request, 'empresa/profile-login.html', {'form': form, 'dados': dados})

def grafico_json(request):
    data = Json_Grafico()
    return JsonResponse(data, safe=False)

def pedidos_json(request):
    data = Json_Pedido()
    return JsonResponse(data, safe=False)


def whastapp(request, pk):
    pedido = Pedido.objects.get(pk=pk)
    num = pedido.cliente.numero
    dado = dict()
    dado.update(enviar_msg(num, pedido))
    return render(request, 'global/whats.html', dado)
