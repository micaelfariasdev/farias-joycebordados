

import datetime
from empresa.models import Pedido
from django.db.models.fields.files import ImageFieldFile


def Json_Grafico():
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

    dic = dict(sorted(dic.items()))

    for dt, qnt in dic.items():
        data.append(qnt)

    return data


def Json_Pedido():
    data = []
    pedidos = Pedido.objects.all()

    for pedido in pedidos:
        dic = {}
        for campo in pedido._meta.fields:
            valor = getattr(pedido, campo.name)

            if hasattr(valor, "id"):
                dic[campo.name] = {"id": valor.id, "nome": str(valor)}
            elif isinstance(valor, (datetime.date, datetime.datetime)):
                dic[campo.name] = valor.isoformat()
            elif isinstance(valor, (ImageFieldFile)):
                pass
            else:
                dic[campo.name] = valor
        data.append(dic.copy())

    return data
