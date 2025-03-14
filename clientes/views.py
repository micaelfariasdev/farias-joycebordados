from django.shortcuts import render
from empresa.models import Empresa, Pedido
# Create your views here.
def PedidoClient(request):
    codigo = request.POST.get('Codigo').strip()
    if codigo[0] == '#':
        codigo = codigo[1:]
    pedido = Pedido.objects.get(codigo=codigo)
    empresa = Empresa.objects.get(pk=1)
    qr_pix = pedido.gerar_qr_pix()

    return render(request, 'clientes/pedido-cliente.html', {'pedido': pedido, 'dados': empresa, 'qr_pix':qr_pix})