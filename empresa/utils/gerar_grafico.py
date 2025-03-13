from empresa.models import Pedido
from django.utils.timezone import now
from django.db.models import Count
from django.db.models.functions import TruncDate
from datetime import timedelta, datetime
from django.db.models import Sum
import locale


def formatar_valor(valor):

    return locale.currency(valor, grouping=True)


def grafico(request):
    # Verifica se 'data_end' foi fornecido, caso contrário, usa a data de hoje
    if not request.GET.get('data_end'):
        hoje = datetime.now()  # Obtém a data e hora atuais
    else:
        hoje = datetime.strptime(request.GET.get('data_end'), '%Y-%m-%d')

    # Se 'data_init' não foi fornecido, usa 7 dias atrás
    if not request.GET.get('data_init'):
        inicio = hoje - timedelta(days=7)
    else:
        inicio = datetime.strptime(request.GET.get('data_init'), '%Y-%m-%d')

    # Calculando o número de dias de diferença
    dias_range = (hoje - inicio).days

    # Obtém os pedidos agrupados por dia
    pedidos_por_dia = (
        Pedido.objects.all()
        .annotate(data_trunc=TruncDate("data"))
        .values("data_trunc")
        .annotate(total_pedidos=Count("id"), total_valor=Sum("valor_total"))
        .filter(data_trunc__range=[inicio, hoje])
        .order_by("data_trunc")
    )

    # Criar listas de datas para o gráfico (últimos 'dias_range' dias)
    datas = [(inicio + timedelta(days=i)).strftime("%d/%m/%Y")
             for i in range(dias_range + 1)]

    # Criar um dicionário com as datas e o total de pedidos
    pedidos_dict = {p["data_trunc"].strftime(
        "%d/%m/%Y"): p["total_pedidos"] for p in pedidos_por_dia}
    valor_dict = {p["data_trunc"].strftime(
        "%d/%m/%Y"): float(p["total_valor"]) for p in pedidos_por_dia}

    # Criar a lista de valores de pedidos para o gráfico
    pedidos_lista = [pedidos_dict.get(data, 0) for data in datas]
    valor_lista = [valor_dict.get(data, 0) for data in datas]

    contexto = {
        "datas": datas,  # Enviar datas formatadas para o template
        "pedidos_lista": pedidos_lista,
        "valor_lista": valor_lista,
    }

    return contexto


def valor_total(request):
    hoje = now()
    ano_atual = hoje.year
    mes_atual = hoje.month

    if not (request.GET.get('data_init') and request.GET.get('data_end')):
        print('aq')
        pedidos_do_mes = Pedido.objects.filter(
            data__year=ano_atual,
            data__month=mes_atual
        )
    else:
        print('aq2123213')
        inicio = datetime.strptime(request.GET.get('data_init'), '%Y-%m-%d')
        final = datetime.strptime(request.GET.get('data_end'), '%Y-%m-%d')
        pedidos_do_mes = Pedido.objects.filter(
            data__range=(
                inicio,
                final + timedelta(days=1)
            )
        )

    faturamento = sum(i.valor_total for i in pedidos_do_mes)
    pedidos = len(pedidos_do_mes)
    ticket_medio = None if pedidos == 0 else faturamento/pedidos
    return {'pedidos': pedidos,
            'faturamento': faturamento,
            'ticket_medio': ticket_medio}


def pages(pages):
    lista = []
    if pages.paginator.num_pages > 4:
        if float(pages.number) == 1:
            for i in range(5):
                lista.append(int(float(pages.number) + i))
        elif float(pages.number) == 2:
            for i in range(-1, 4):
                lista.append(int(float(pages.number) + i))
        elif float(pages.number) == float(pages.paginator.num_pages):
            for i in range(-4, 1):
                lista.append(int(float(pages.number) + i))
        elif float(pages.number) == float(pages.paginator.num_pages) - 1:
            for i in range(-3, 2):
                lista.append(int(float(pages.number) + i))
        elif float(pages.number) == float(pages.paginator.num_pages) - 2:
            for i in range(-2, 3):
                lista.append(int(float(pages.number) + i))
        else:
            for i in range(-2, 3):
                lista.append(int(float(pages.number) + i))
        return lista
    else:
        return [i for i in range(1, pages.paginator.num_pages)]
