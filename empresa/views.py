from django.shortcuts import render, redirect, get_object_or_404
from .models import Empresa, Pedido
from .forms import PedidosForm
from .utils import grafico


def ProfileView(request):
    dados = Empresa.objects.get(pk=1)
    pedidos = Pedido.objects.all()
    valor_total = 0
    for pedido in pedidos:
        valor_total += pedido.valor_total
    contexto = {'dados': dados, 'pedidos': pedidos, 'faturamento': valor_total}
    contexto.update(grafico(inicio=request.GET.get(
        'inicio'), final=request.GET.get('final')))
    print(contexto)
    return render(request, 'empresa/profile-detail.html', context=contexto)


def PedidosListView(request):
    dados = Empresa.objects.get(pk=1)
    pedidos = Pedido.objects.all().order_by('status')
    return render(request, 'joycebordados/pedidos.html', {'dados': dados, 'pedidos': pedidos})


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
