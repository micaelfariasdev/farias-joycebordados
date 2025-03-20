from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from empresa.models import Empresa, Pedido
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


@csrf_exempt
def PedidoClient(request, cod=None):
    if request.method == 'GET':
        codigo_ = request.GET.get('codigo').strip()
    elif cod:
        codigo_ = cod  # Evita erro se for None

    if not codigo_:
        # Retorna erro 400 se o código estiver vazio
        return HttpResponseBadRequest("Código inválido.")

    if codigo_.startswith('#'):
        codigo_ = codigo_[1:]

    # Garante que retorna 404 se não encontrar
    pedido = get_object_or_404(Pedido, codigo=codigo_)
    empresa = get_object_or_404(Empresa, pk=1)

    qr_pix = pedido.gerar_qr_pix()

    return render(request, 'clientes/pedido-cliente.html', {'pedido': pedido, 'dados': empresa, 'qr_pix': qr_pix})


def orcamento(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        telefone = request.POST.get("telefone")
        mensagem = request.POST.get("mensagem")

        assunto = f"Solicitação de orçamento de {nome}"
        corpo = f"""
Nome: {nome}
Email: {email}
Telefone: {telefone}

Mensagem:
{mensagem}
        """

        send_mail(
            assunto,
            corpo,
            "micaelfarias.dev@gmail.com",  # Remetente
            ["contato@fariasfardas.com"],  # Destinatário
            fail_silently=False,
        )

        # Crie uma página de sucesso para redirecionamento
        return redirect("joycebordados:home")

    return render(request, "orcamento.html")  # Substitua pelo seu template
