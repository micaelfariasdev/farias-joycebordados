from empresa.models import Pedido
from django.utils.timezone import now
from django.db.models import Count
from django.db.models.functions import TruncDate
from datetime import timedelta, datetime


def grafico(inicio=None, final=None):
    # Verifica se 'final' foi fornecido, caso contrário, usa a data de hoje
    if final == '' or final == None:
        hoje = now()  # Obtém a data e hora atuais (datetime)
    else:
        final = datetime.strptime(final, '%Y-%m-%d')
        hoje = final

    # Obtém os pedidos agrupados por dia
    pedidos_por_dia = (
        Pedido.objects.all()
        .annotate(data_trunc=TruncDate("data"))
        .values("data_trunc")
        .annotate(total=Count("id"))
        .order_by("data_trunc")
    )

    # Verificar se há pedidos no banco
    if pedidos_por_dia.exists():
        if inicio == '' or inicio == None:
            # Se 'inicio' não foi informado, usa 7 dias atrás
            dia = hoje - timedelta(days=7)
        else:
            inicio = datetime.strptime(inicio, '%Y-%m-%d')
            dia = inicio  # Converte 'inicio' para datetime

        # Calculando o número de dias de diferença
        # Isso agora deve funcionar corretamente
        dias_range = (hoje - dia).days
    else:
        # Caso não haja pedidos, retornar listas vazias
        return {"datas": [], "pedidos_lista": []}

    # Criar listas de datas para o gráfico (últimos 'dias_range' dias)
    datas = [(dia + timedelta(days=i)).strftime("%d/%m/%Y")
             for i in range(dias_range+1)]

    # Criar um dicionário com as datas e o total de pedidos
    pedidos_dict = {p["data_trunc"].strftime(
        "%d/%m/%Y"): p["total"] for p in pedidos_por_dia}

    # Criar a lista de valores de pedidos para o gráfico
    pedidos_lista = [pedidos_dict.get(data, 0) for data in datas]

    contexto = {
        "datas": datas,  # Enviar datas formatadas para o template
        "pedidos_lista": pedidos_lista,  # Enviar contagem de pedidos
    }

    return contexto
