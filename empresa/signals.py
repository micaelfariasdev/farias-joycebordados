from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.forms.models import model_to_dict
from .models import Pedido, HistoricoPedido
from .utils import replacehist


@receiver(pre_save, sender=Pedido)
def salvar_historico_pedido(sender, instance, **kwargs):
    if instance.pk:  # Se o pedido já existe (edição)
        pedido_antigo = Pedido.objects.get(pk=instance.pk)
        dados_antigos = model_to_dict(pedido_antigo)
        dados_novos = model_to_dict(instance)

        alteracoes = {}
        for campo in dados_novos:
            if dados_antigos.get(campo) != dados_novos[campo]:
                alteracoes[replacehist(campo)] = {
                    "antes": replacehist(dados_antigos.get(campo)),
                    "depois": replacehist(dados_novos[campo])
                }

        if alteracoes:
            HistoricoPedido.objects.create(
                pedido=instance,
                alteracoes=alteracoes
            )


@receiver(post_save, sender=Pedido)
def salvar_historico_pedido(sender, instance, created, **kwargs):
    if created:  # Se for um novo pedido
        HistoricoPedido.objects.create(
            pedido=instance,
            alteracoes={"Criação": {"criacao": "Pedido criado com sucesso"}}
        )
        return

    pedido_antigo = Pedido.objects.filter(pk=instance.pk).first()
    if not pedido_antigo:
        return

    dados_antigos = model_to_dict(pedido_antigo)
    dados_novos = model_to_dict(instance)

    alteracoes = {
        replacehist(campo): {
            "antes": replacehist(dados_antigos.get(campo, "")),
            "depois": replacehist(dados_novos[campo])
        }
        for campo in dados_novos if dados_antigos.get(campo) != dados_novos[campo]
    }

    if alteracoes:  # Só cria o histórico se houver mudanças
        HistoricoPedido.objects.create(
            pedido=instance,
            alteracoes=alteracoes
        )
