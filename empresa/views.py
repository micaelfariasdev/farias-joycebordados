from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from .models import Empresa, Pedido
from .forms import PedidosForm


class ModelDetailView(DetailView):
    model = Empresa
    template_name = ".html"


def PedidosListView(request):
    dados = Empresa.objects.get(pk=1)
    pedidos = Pedido.objects.all().order_by('status')
    return render(request, 'joycebordados/pedidos.html', {'dados':dados, 'pedidos': pedidos})

def PedidodetailView(request, pk):
    dados = Empresa.objects.get(pk=1)
    pedido = Pedido.objects.get(pk=pk)
    form =  PedidosForm(instance=pedido)
    return render(request, 'joycebordados/pedido-detail.html', {'dados':dados, 'pedido': pedido, 'form': form})

def PedidoEditView(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    
    if request.method == "POST":
        form = PedidosForm(request.POST or None, instance=pedido)
        if form.is_valid():
            form.save()
            return redirect('empresa:pedidos')  # Redireciona para a lista de pedidos após salvar
        else:
            # Caso o formulário não seja válido, você pode logar os erros, mas o retorno será um erro 400
            print(form.errors)  # (Opcional) Para depuração
            return redirect('empresa:pedidos')  # Ou você pode retornar um redirect mesmo com erro, ou renderizar o mesmo formulário com erros.

    return redirect('empresa:pedidos')