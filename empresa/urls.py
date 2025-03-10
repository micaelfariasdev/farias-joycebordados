
from .views import PedidosListView, PedidodetailView, PedidoEditView, ProfileView
from django.urls import path

app_name = 'empresa'

urlpatterns = [
    path('', ProfileView, name='empresa'),
    path('pedidos/', PedidosListView, name='pedidos'),
    path('pedidos/<int:pk>', PedidodetailView, name='detail-pedido'),
    path('pedidos/<int:pk>/edit', PedidoEditView, name='pedido-edit'),
]
