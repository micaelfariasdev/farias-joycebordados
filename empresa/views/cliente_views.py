from django.shortcuts import render, redirect
from ..forms import ClienteForm
from ..models import Cliente
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def ClientesListView(request):
    formcliente = ClienteForm()
    if request.method == "POST":
        formcliente = ClienteForm(request.POST)
        if formcliente.is_valid:
            formcliente.save()
    return render(request, 'empresa/clientes.html', {'formcliente':formcliente})

def EditCliente(request, pk):
    cliente = Cliente.objects.get(pk=pk)
    formcliente = ClienteForm(instance=cliente)
    
    if request.method == "POST":
        formcliente = ClienteForm(request.POST, instance=cliente)  # Atualiza a instância do cliente
        if formcliente.is_valid():  # Chama o método is_valid() corretamente
            formcliente.save()
            return redirect('adm:fechar_pagina')  # Redireciona após salvar
            
    return render(request, 'empresa/cliente-new.html', {'formcliente': formcliente})