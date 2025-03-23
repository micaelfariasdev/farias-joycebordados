
from django.contrib.auth.decorators import login_required
from .. import views
from django.urls import path

app_name = 'adm'

urlpatterns = [
    path('profile/pedidos/', login_required(views.PedidosListView), name='pedidos'),
    path('profile/pedidos/new/',
         login_required(views.PedidoNewView), name='new-pedido'),
    path('profile/pedidos/new/save',
         login_required(views.PedidoNewSaveView), name='save-pedido'),
    path('profile/grafico/api/',
         login_required(views.grafico_json), name='pedido-api'),
    path('profile/pedidos/api/',
         login_required(views.pedidos_json), name='pedido-api'),
    path('profile/pedidos/<int:pk>/',
         login_required(views.PedidodetailView), name='detail-pedido'),
    path('profile/pedidos/<int:pk>/edit/',
         login_required(views.PedidoEditView), name='pedido-edit'),
    path('profile/pedidos/<int:pk>/del/',
         login_required(views.PedidoDelView), name='pedido-del'),
]
