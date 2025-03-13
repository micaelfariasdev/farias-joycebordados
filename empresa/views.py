from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from .models import Empresa, Pedido
from .forms import PedidosForm, FilterForm
from .utils import grafico, valor_total
from django.db.models.functions import TruncDate
from datetime import timedelta, datetime


def ProfileView(request):
    dados = Empresa.objects.get(pk=1)

    filter = {
        'data_init': request.GET.get('data_init') or (datetime(now().year, now().month, 1)).strftime('%Y-%m-%d'),
        'data_end': request.GET.get('data_end') or (datetime.now()).strftime('%Y-%m-%d')
    }
    contexto = {'dados': dados}
    contexto.update(valor_total(request))
    contexto.update(grafico(request))
    form = FilterForm(initial=filter)
    contexto.update({'form': form})
    return render(request, 'empresa/profile-detail.html', context=contexto)


def PedidosListView(request):
    dados = Empresa.objects.get(pk=1)
    pedidos = Pedido.objects.all().order_by('status')
    return render(request, 'empresa/pedido-profile.html', {'dados': dados, 'pedidos': pedidos})


def PedidodetailView(request, pk):
    dados = Empresa.objects.get(pk=1)
    pedido = Pedido.objects.get(pk=pk)
    form = PedidosForm(instance=pedido)
    return render(request, 'joycebordados/pedido-detail.html', {'dados': dados, 'pedido': pedido, 'form': form})


def PedidoEditView(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)

    if request.method == "POST":
        form = PedidosForm(request.POST or None, instance=pedido)
        if form.is_valid():
            form.save()
            # Redireciona para a lista de pedidos após salvar
            return redirect('empresa:pedidos')
        else:
            # Caso o formulário não seja válido, você pode logar os erros, mas o retorno será um erro 400
            print(form.errors)  # (Opcional) Para depuração
            # Ou você pode retornar um redirect mesmo com erro, ou renderizar o mesmo formulário com erros.
            return redirect('empresa:pedidos')

    return redirect('empresa:pedidos')
