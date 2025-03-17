from django.shortcuts import render, redirect
from .forms import CustomLoginForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from .models import Empresa, Pedido, FotosCarrossel
from .forms import PedidosForm, FilterForm, ProcurarForm, EmpresaForm, FotosCarrosselForm
from .utils import grafico, valor_total, pages
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q


def DashBoardView(request):
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
        filtro_q = Q(codigo__icontains=pesquisa) | Q(
            cliente__nome__icontains=pesquisa)

    if pg in ["True", "False"]:  # Garantir que é um valor booleano válido
        filtro_pg = Q(pago=(pg))

    if status:
        filtro_est = Q(status=status)

    dados = Empresa.objects.get(pk=1)
    pedidos = Pedido.objects.filter(
        filtro_q & filtro_pg & filtro_est).order_by('status', '-id')

    form = ProcurarForm(request.GET or None)

    return render(request, 'empresa/profile-pedidos.html', { 'form': form, 'dados': dados, 'pedidos': pedidos,})


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
            # Redireciona para a lista de pedidos após salvar
            return redirect('empresa:pedidos')
        else:
            # Caso o formulário não seja válido, você pode logar os erros, mas o retorno será um erro 400
            print(form.errors)  # (Opcional) Para depuração
            # Ou você pode retornar um redirect mesmo com erro, ou renderizar o mesmo formulário com erros.
            return redirect('empresa:pedidos')

    return redirect('empresa:pedidos')


def DadosProfileView(request):
    dados = Empresa.objects.get(pk=1)
    form = EmpresaForm(instance=dados)

    return render(request, 'empresa/profile-dados.html', {'dados': dados, 'form': form})


def CarrosselProfileView(request):
    dados = Empresa.objects.get(pk=1)
    fotos = dados.fotos_carrossel.all()
    form = FotosCarrosselForm(initial={'empresa': dados})
    return render(request, 'empresa/profile-carrosel.html', {'dados': dados, 'form': form, 'fotos': fotos})


def DelFotoCarroselView(request, pk):
    foto = get_object_or_404(FotosCarrossel, pk=pk)
    foto.delete()
    return redirect('empresa:carrossel')


def Login(request):
    dados = Empresa.objects.get(pk=1)
    if request.method == 'POST':
        form = CustomLoginForm(request=request, data=request.POST)
        if form.is_valid():
            # Verifica as credenciais e loga o usuário
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                # Redireciona para o dashboard ou página principal
                return redirect('empresa:empresa')
            else:
                # Se as credenciais forem inválidas
                form.add_error(None, 'Usuário ou senha inválidos')
        else:
            # Se o formulário não for válido
            form.add_error(None, 'Erro no formulário de login')
    else:
        form = CustomLoginForm()

    return render(request, 'empresa/profile-login.html', {'form': form, 'dados': dados})


def AddFotoCarroselView(request):
    if request.method == "POST":
        form = FotosCarrosselForm(request.POST or None,
                                  request.FILES or None,)
        if form.is_valid():
            form.save()
            print('salvo')
            # Redireciona para a lista de pedidos após salvar
            return redirect('empresa:carrossel')
        else:
            # Caso o formulário não seja válido, você pode logar os erros, mas o retorno será um erro 400
            print(form.errors)  # (Opcional) Para depuração
            # Ou você pode retornar um redirect mesmo com erro, ou renderizar o mesmo formulário com erros.
            return redirect('empresa:carrossel')
    return redirect('empresa:carrossel')


def DadosEditView(request):
    dados = get_object_or_404(Empresa, pk=1)
    if request.method == "POST":
        form = EmpresaForm(request.POST or None,
                           request.FILES or None, instance=dados)
        if form.is_valid():
            form.save()
            print('salvo')
            # Redireciona para a lista de pedidos após salvar
            return redirect('empresa:dados')
        else:
            # Caso o formulário não seja válido, você pode logar os erros, mas o retorno será um erro 400
            print(form.errors)  # (Opcional) Para depuração
            # Ou você pode retornar um redirect mesmo com erro, ou renderizar o mesmo formulário com erros.
            return redirect('empresa:dados')

    return redirect('empresa:dados')
