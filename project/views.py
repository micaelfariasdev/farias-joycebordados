from django.shortcuts import redirect


def red(request, cod):
    return redirect(f'/cliente/pedido/?codigo={cod}')
