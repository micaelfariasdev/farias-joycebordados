

from empresa.models import Pedido


def gerar_json():
    dic = {}
    data = []
    pedidos = Pedido.objects.all()

    for pedido in pedidos:
        date = pedido.data.strftime('%Y-%m-%d')

        if date not in dic:
            dic[date] = {'data': date, 'quantidade': 1,
                         'valor': pedido.valor_total}
        else:
            dic[date]['quantidade'] += 1
            dic[date]['valor'] += pedido.valor_total

    # Ordena os pedidos por data
    dic = dict(sorted(dic.items()))

    # Converte o dicionário para uma lista de dicionários
    for dt, qnt in dic.items():
        data.append(qnt)

    return data
