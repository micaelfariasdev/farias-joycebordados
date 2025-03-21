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
    dicionario = {
        'True': 'Pago',
        'False': 'Pagamento Pendente',
        '0-pendente': 'Pedido Pendente',
        '0-pendente': 'Pedido Pendente',
        '1-producao': 'Produção',
        '2-pronto': 'Pronto para entrega',
        '3-entregue': 'Pedido Finalizado',
        'data_entrega': 'Data de entrega',
        'produto': 'Produto',
        'quantidade':  'Quantidade',
        'valor': 'Valor unitário',
        'observacao': 'Descrição do pedido',
        'status': 'Status do pedidoo',
        'pago': 'Status de pagamento',
    }

    if isinstance(campo, Decimal):
        campo = locale.currency(campo, grouping=True)
        return campo
    else:
        for campodic, valordic in dicionario.items():
            if campo == campodic:
                return valordic

    return campo
