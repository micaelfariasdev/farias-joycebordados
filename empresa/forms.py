from django import forms
from .models import Pedido, Empresa, FotosCarrossel
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.contrib import admin

class PedidosForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'
    empresa = forms.ModelChoiceField(queryset=Empresa.objects.all(), initial=Empresa.objects.get(pk=1))
    quantidade = forms.IntegerField(required=False)
    valor = forms.FloatField(required=False)
    codigo = forms.CharField(required=False)
    data_entrega = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        rel_field = Pedido._meta.get_field('cliente')  # Campo relacionado
        self.fields['cliente'].widget = RelatedFieldWidgetWrapper(
            self.fields['cliente'].widget, rel_field.remote_field, admin.site
        )


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = '__all__'


class FotosCarrosselForm(forms.ModelForm):

    class Meta:
        model = FotosCarrossel
        # Apenas os campos que desejo exibir no formulário
        fields = '__all__'

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Usuário'}),
        max_length=100
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}),
        max_length=100
    )

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
