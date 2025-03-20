from .json_generation import *
from .whatsapp import *
from calendar import monthrange
import locale
from decimal import Decimal
# Define o locale para o Brasil (moeda em reais)
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def ultimo_dia_mes(year, month):
    return monthrange(year, month)[1]


def replacehist(campo):
    if campo == 'True':
        return 'Pago'
    if campo == 'False':
        return 'Pagamento Pendente'
    if isinstance(campo, Decimal):
        campo = locale.currency(campo, grouping=True)
        return campo
    if campo == '0-pendente':
        return 'Pedido Pendente'
    if campo == '1-producao':
        return 'Produção'
    if campo == '2-pronto':
        return 'Pronto para entrega'
    if campo == '3-entregue':
        return 'Pedido Finalizado'
    return 'ERRO'