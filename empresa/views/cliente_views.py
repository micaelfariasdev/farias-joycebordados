from django.shortcuts import render, redirect
from ..forms import ClienteForm
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def NewCliente(request):
    formcliente = ClienteForm()
    if request.method == "POST":
        formcliente = ClienteForm(request.POST)
        if formcliente.is_valid:
            formcliente.save()
            return redirect('adm:fechar_pagina')

    return render(request, 'empresa/cliente-new.html', {'formcliente':formcliente})
