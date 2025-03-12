# meuapp/templatetags/filtros.py
import locale
from django import template

register = template.Library()


@register.filter
def formatar_telefone(telefone):
    """Formata um número de telefone no formato (XX) XXXXX-XXXX"""
    telefone = str(telefone)  # Garantir que o telefone seja uma string
    # Caso padrão para números com 10 dígitos
    return f"({telefone[:2]}) {telefone[2:3]} {telefone[3:7]}-{telefone[7:]}"
    # Se o número não for válido, retorne sem formatação


# Configura o locale para o Brasil (para que a vírgula seja usada como separador decimal)
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


@register.filter
def monetario(valor):
    valor = float(valor)
    # Formata o valor como uma string com separadores de milhar
    return locale.currency(valor, grouping=True)


@register.filter
def dividir(valor, divisor):
    try:
        return valor / divisor
    except ZeroDivisionError:
        return 0  # Retorna 0 se houver divisão por zero
