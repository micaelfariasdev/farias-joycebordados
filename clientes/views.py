from django.core.mail import send_mail
from django.shortcuts import render, redirect
from empresa.models import Empresa, Pedido
# Create your views here.


def PedidoClient(request):
    codigo = request.POST.get('Codigo').strip()
    if codigo[0] == '#':
        codigo = codigo[1:]
    pedido = Pedido.objects.get(codigo=codigo)
    empresa = Empresa.objects.get(pk=1)
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
