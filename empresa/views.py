from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from .models import Empresa, Pedido
from .forms import PedidosForm, FilterForm, ProcurarForm
from .utils import grafico, valor_total, pages
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q


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
    pesquisa = request.GET.get('q', '').strip()
    pg = request.GET.get('pago', '').strip()
    status = request.GET.get('status', '').strip()
    filtro_q = Q()
    filtro_pg = Q()
    filtro_est = Q()

    if pesquisa:
        filtro_q = Q(codigo__icontains=pesquisa) | Q(cliente__nome__icontains=pesquisa)

    if pg in ["True", "False"]:  # Garantir que é um valor booleano válido
        filtro_pg = Q(pago=(pg))

    if status:
        filtro_est = Q(status=status)

    dados = Empresa.objects.get(pk=1)
    pedidos = Pedido.objects.filter(filtro_q & filtro_pg & filtro_est).order_by('status', '-id')


    paginator = Paginator(pedidos, 8)
    form = ProcurarForm(request.GET or None)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    pages_nav = pages(page_obj)

    query_params = request.GET.copy()
    query_params.pop('page', None)  # Remove 'page' para evitar conflitos ao paginar
    query_string = query_params.urlencode()
    return render(request, 'empresa/pedido-profile.html', {'query_string':query_string,'form': form, 'dados': dados, 'pedidos': page_obj, 'page_obj': page_obj, 'pages_nav': pages_nav})


def PedidodetailView(request, pk):
    dados = Empresa.objects.get(pk=1)
    pedido = Pedido.objects.get(pk=pk)
    form = PedidosForm(instance=pedido)

    return render(request, 'joycebordados/pedido-detail.html', {'dados': dados, 'pedido': pedido, 'form': form,})


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


