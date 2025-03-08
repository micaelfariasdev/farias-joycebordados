# meuapp/templatetags/filtros.py
from django import template

register = template.Library()

@register.filter
def formatar_telefone(telefone):
    """Formata um número de telefone no formato (XX) XXXXX-XXXX"""
    telefone = str(telefone)  # Garantir que o telefone seja uma string
      # Caso padrão para números com 10 dígitos
    return f"({telefone[:2]}) {telefone[2:3]} {telefone[3:7]}-{telefone[7:]}"
     # Se o número não for válido, retorne sem formatação
