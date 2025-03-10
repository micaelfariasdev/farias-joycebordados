from empresa.models import Pedido
from datetime import timedelta
from django.utils.timezone import now



def grafico():
    hoje = now().date()
    dias_30 = hoje - timedelta(days=30)


    pedidos = Pedido.objects.filter(data_pedido__range=[dias_30, hoje])
    return pedidos

grafico()