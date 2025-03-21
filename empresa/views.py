from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render, redirect
from .forms import CustomLoginForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from .models import Empresa, Pedido, FotosCarrossel
from .forms import PedidosForm, FilterForm, ProcurarForm, EmpresaForm, FotosCarrosselForm
from .utils import gerar_json, enviar_msg
from datetime import datetime
from dateutil.relativedelta import relativedelta
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def fechar_pagina(request):

    return render(request, 'global/fechar.html')


def DashBoardView(request):

    dados = Empresa.objects.get(pk=1)

    filter = {
        'data_init': request.GET.get('data_init') or (datetime(now().year, now().month, 1)).strftime('%Y-%m-%d'),
        'data_end': request.GET.get('data_end') or (datetime.now()).strftime('%Y-%m-%d')
    }

    # Se os valores vindos do GET forem strings, converter para datetime
    if isinstance(filter['data_init'], str):
        filter['data_init'] = datetime.strptime(
            filter['data_init'], '%Y-%m-%d')
    if isinstance(filter['data_end'], str):
        filter['data_end'] = datetime.strptime(filter['data_end'], '%Y-%m-%d')
    dif_days = filter['data_end'] - filter['data_init']
    filtercompare = {
        'data_init': (filter['data_init'] - relativedelta(months=1)),
        'data_end': (filter['data_init'] - relativedelta(months=1) + dif_days)
    }
    if filtercompare['data_end'] > filter['data_init']:
        filtercompare['data_end'] = (
            filter['data_init'] - relativedelta(days=1))

    filter['data_init'] = filter['data_init'].strftime('%Y-%m-%d')
    filter['data_end'] = filter['data_end'].strftime('%Y-%m-%d')
    filtercompare['data_init'] = filtercompare['data_init'].strftime(
        '%Y-%m-%d')
    filtercompare['data_end'] = filtercompare['data_end'].strftime('%Y-%m-%d')

    contexto = {'dados': dados, 'filter': filter}
    form = FilterForm(initial=filter)
    form2 = FilterForm(initial=filtercompare)
    contexto.update({'form': form, 'form2': form2})
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
            # Redireciona para a lista de pedidos após salvar
            return redirect('adm:fechar_pagina')
        else:
            # Caso o formulário não seja válido, você pode logar os erros, mas o retorno será um erro 400
            print(form.errors)  # (Opcional) Para depuração
            # Ou você pode retornar um redirect mesmo com erro, ou renderizar o mesmo formulário com erros.
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
    return render(request, 'empresa/pedido-new.html', {'dados': dados, 'form': form, })


def PedidoNewSaveView(request):

    form = PedidosForm()
    if request.method == "POST":
        if request.method == 'POST':
            form = PedidosForm(request.POST)

            if form.is_valid():  # ✅ Verifica se o formulário é válido
                # Salva sem enviar ao banco ainda
                pedido = form.save(commit=False)
                pedido.save()
                # Agora salva no banco
                return redirect('adm:fechar_pagina')
            else:
                return render(request, 'empresa/pedido-new.html', {'form': form})


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
    return redirect('adm:carrossel')


def Login(request):
    if request.user.is_authenticated:
        return redirect('adm:empresa')
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
                return redirect('adm:empresa')
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
            return redirect('adm:carrossel')
        else:
            # Caso o formulário não seja válido, você pode logar os erros, mas o retorno será um erro 400
            print(form.errors)  # (Opcional) Para depuração
            # Ou você pode retornar um redirect mesmo com erro, ou renderizar o mesmo formulário com erros.
            return redirect('adm:carrossel')
    return redirect('adm:carrossel')


def DadosEditView(request):

    dados = get_object_or_404(Empresa, pk=1)
    if request.method == "POST":
        form = EmpresaForm(request.POST or None,
                           request.FILES or None, instance=dados)
        if form.is_valid():
            form.save()
            print('salvo')
            # Redireciona para a lista de pedidos após salvar
            return redirect('adm:dados')
        else:
            # Caso o formulário não seja válido, você pode logar os erros, mas o retorno será um erro 400
            print(form.errors)  # (Opcional) Para depuração
            # Ou você pode retornar um redirect mesmo com erro, ou renderizar o mesmo formulário com erros.
            return redirect('adm:dados')

    return redirect('adm:dados')


def pedidos_json(request):

    data = gerar_json()
    # Retorna a resposta JSON
    return JsonResponse(data, safe=False)


def whastapp(request, pk):

    pedido = Pedido.objects.get(pk=pk)
    num = pedido.cliente.numero
    dado = dict()
    dado.update(enviar_msg(num, pedido))
    return render(request, 'global/whats.html', dado)
