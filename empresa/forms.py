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


class ProcurarForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Buscar pedido...'}
        )
    )
    status = forms.ChoiceField(
        required=False,
        choices=[
            ('0-pendente', 'Pendente'),
            ('1-producao', 'Produção'),
            ('2-pronto', 'Pronto para entrega'),
            ('3-entregue', 'Finalizado')
        ],
        widget=forms.RadioSelect,
        label='Status:'
    )

    pago = forms.ChoiceField(
        required=False,
        choices=[
            (True, 'Pago'),
            (False, 'Falta pagar')
        ],
        label='Pago:',
        widget=forms.RadioSelect,
    )
