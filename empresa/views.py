from django.shortcuts import render, redirect, get_object_or_404
from .models import Empresa, Pedido, FotosCarrossel
from .forms import PedidosForm, EmpresaForm, FotosCarrosselForm
from django.utils.timezone import now
from django.db.models import Count
from django.db.models.functions import TruncDate
from datetime import timedelta


def grafico():
    hoje = now().date()
    semana = hoje - timedelta(days=8)

    pedidos_por_dia = (
        Pedido.objects.filter(data__gte=semana)  # Filtra os últimos 30 dias
        .annotate(data_trunc=TruncDate("data"))  # Agrupa por data sem horário
        .values("data_trunc")
        .annotate(total=Count("id"))  # Conta pedidos por dia
        .order_by("data_trunc")
    )

    # Criar listas para o gráfico
    datas = [str(semana + timedelta(days=i)) for i in range(9)]  # Lista com todas as datas
    pedidos_dict = {str(p["data_trunc"]): p["total"] for p in pedidos_por_dia}  # Dicionário com contagem de pedidos

    # Criar lista de valores para o gráfico
    pedidos_lista = [pedidos_dict.get(data, 0) for data in datas]  

    contexto = {
        "datas": datas,  # Enviar datas formatadas para o template
        "pedidos_lista": pedidos_lista,  # Enviar contagem de pedidos
    }
    return contexto


def ProfileView(request):
    dados = Empresa.objects.get(pk=1)
    pedidos = Pedido.objects.all()
    valor_total = 0
    for pedido in pedidos:
        valor_total += pedido.valor_total
    contexto = {'dados': dados, 'pedidos': pedidos, 'faturamento': valor_total}
    contexto.update(grafico())
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
