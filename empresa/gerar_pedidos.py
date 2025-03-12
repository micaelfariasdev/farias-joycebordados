import random
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from .models import Cliente, Pedido


def criar_pedidos_aleatorios(qtd=10):
    """Cria pedidos aleatórios até a data de hoje"""
    clientes = list(Cliente.objects.all())
    if not clientes:
        print("Nenhum cliente cadastrado.")
        return

    produtos = ["Bordado", "Camisa de Evento", "Uniforme Profissional"]
    status_opcoes = ["0-pendente", "1-producao", "2-pronto", "3-entregue"]
    hoje = datetime.today()
        # Definir o intervalo de datas
    inicio = datetime(2025, 1, 1)  # 1º de janeiro de 2025
    fim = datetime(2025, 12, 13)  # 13º de dezembro de 2025

    # Calcular o número de dias entre o início e o fim
    delta = fim - inicio

    # Gerar um número aleatório de dias dentro desse intervalo
    dias_aleatorios = random.randint(0, delta.days)

    # Gerar a data final somando os dias aleatórios ao início
    data_aleatoria = inicio + timedelta(days=dias_aleatorios)

    # Tornar a data "aware" (com fuso horário)
    data_aware = make_aware(data_aleatoria)

    for _ in range(qtd):
        cliente = random.choice(clientes)
        # Pedidos podem ter até 60 dias de antiguidade
        dias_atras = random.randint(0, 60)
        data_pedido = data_aware
        data_entrega = data_pedido + \
            timedelta(days=random.randint(1, 30)
                      ) if random.random() > 0.5 else None

        quantidade = random.randint(1, 10)
        valor = round(random.uniform(10, 200), 2)
        valor_total = quantidade * valor
        status = random.choice(status_opcoes)
        pago = random.choice([True, False])

        pedido = Pedido(
            cliente=cliente,
            data=data_aware,
            data_entrega=data_entrega,
            produto=random.choice(produtos),
            quantidade=quantidade,
            valor=valor,
            valor_total=valor_total,
            status=status,
            pago=pago,
        )
        pedido.save()

    print(f"{qtd} pedidos gerados com sucesso!")
