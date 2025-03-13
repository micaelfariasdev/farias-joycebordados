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
    excluir = forms.BooleanField(
        required=False, label="Excluir")  # Campo para exclusão

    class Meta:
        model = FotosCarrossel
        # Apenas os campos que desejo exibir no formulário
        fields = ['foto', 'excluir']


class FilterForm(forms.Form):
    data_init = forms.DateField(
        required=True,
        label='Data de Inicio',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    data_end = forms.DateField(
        required=True,
        label='Data Final',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
