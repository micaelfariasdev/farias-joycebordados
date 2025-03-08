from django import forms
from .models import Pedido


class PedidosForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'
