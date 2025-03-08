
from .views import ModelDetailView, PedidosListView, PedidodetailView, PedidoEditView
from django.urls import path

app_name = 'empresa'

urlpatterns = [
    path('', ModelDetailView.as_view(), name='empresa'),
    path('pedidos/', PedidosListView, name='pedidos'),
    path('pedidos/<int:pk>', PedidodetailView, name='detail-pedido'),
    path('pedidos/<int:pk>/edit', PedidoEditView, name='pedido-edit'),
]
