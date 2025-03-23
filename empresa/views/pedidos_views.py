from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from ..models import Empresa, Pedido
from ..forms import PedidosForm, ProcurarForm, ClienteForm
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def PedidosListView(request):
    pesquisa = request.GET.get('q', '').strip()
    pg = request.GET.get('pago', '').strip()
    status = request.GET.get('status', '').strip()
    filtro_q = Q()
    filtro_pg = Q()
    filtro_est = Q()
    if pesquisa:
        filtro_q = Q(codigo__icontains=pesquisa) | Q(
            cliente__nome__icontains=pesquisa)
    if pg in ["True", "False"]:  
        filtro_pg = Q(pago=(pg))
    if status:
        filtro_est = Q(status=status)
    dados = Empresa.objects.get(pk=1)
    pedidos = Pedido.objects.filter(
        filtro_q & filtro_pg & filtro_est).order_by('status', '-id')
    form = ProcurarForm(request.GET or None)
    return render(request, 'empresa/profile-pedidos.html', {'form': form, 'dados': dados, 'pedidos': pedidos, })

def PedidodetailView(request, pk):
    dados = Empresa.objects.get(pk=1)
    pedido = Pedido.objects.get(pk=pk)
    form = PedidosForm(instance=pedido)
    return render(request, 'empresa/pedido-detail.html', {'dados': dados, 'pedido': pedido, 'form': form, })

def PedidoEditView(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == "POST":
        form = PedidosForm(request.POST or None, instance=pedido)
        if form.is_valid():
            form.save()
            return redirect('adm:fechar_pagina')
        else:
            print(form.errors)  
            return redirect('adm:pedidos')
    return redirect('adm:pedidos')


def PedidoDelView(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == "POST":
        pedido.delete()
        return redirect('adm:fechar_pagina')
    return redirect('adm:pedidos')


def PedidoNewView(request):
    dados = Empresa.objects.get(pk=1)
    form = PedidosForm()
    formcliente = ClienteForm()
    if request.method == 'POST':
        formcliente = ClienteForm(request.POST)
        if formcliente.is_valid():  
            formcliente.save()
    return render(request, 'empresa/pedido-new.html', {'dados': dados, 'form': form, 'formcliente':formcliente})


def PedidoNewSaveView(request):
    form = PedidosForm()
    if request.method == "POST":
        if request.method == 'POST':
            form = PedidosForm(request.POST)
            if form.is_valid():  
                pedido = form.save(commit=False)
                pedido.save()
                return redirect('adm:fechar_pagina')
            else:
                return render(request, 'empresa/pedido-new.html', {'form': form})

