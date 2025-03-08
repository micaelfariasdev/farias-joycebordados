
from .views import PedidoClient
from django.urls import path

app_name = 'cliente'

urlpatterns = [
    path('pedido/', PedidoClient, name='pedido-cliente'),
]
