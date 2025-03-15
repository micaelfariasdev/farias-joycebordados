
from .views import PedidoClient, orcamento
from django.urls import path

app_name = 'cliente'

urlpatterns = [
    path('pedido/', PedidoClient, name='pedido-cliente'),
    path("orcamento/", orcamento, name="orcamento"),
]
