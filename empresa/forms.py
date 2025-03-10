from django import forms
from .models import Pedido, Empresa, FotosCarrossel


class PedidosForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = '__all__'


class FotosCarrosselForm(forms.ModelForm):
    excluir = forms.BooleanField(required=False, label="Excluir")  # Campo para exclusão

    class Meta:
        model = FotosCarrossel
        fields = ['foto', 'excluir']  # Apenas os campos que desejo exibir no formulário
