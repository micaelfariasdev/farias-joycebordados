
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path

app_name = 'empresa'

urlpatterns = [
    path('login/', views.Login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', login_required(views.DashBoardView), name='empresa'),
    path('config/', login_required(views.DadosProfileView), name='dados'),
    path('config/edit/', login_required(views.DadosEditView), name='dados-edit'),
    path('carrossel/', login_required(views.CarrosselProfileView), name='carrossel'),
    path('pedidos/', login_required(views.PedidosListView), name='pedidos'),
    path('pedidos/<int:pk>/', login_required(views.PedidodetailView),
         name='detail-pedido'),
    path('pedidos/new/', login_required(views.PedidoNewView),
         name='new-pedido'),
    path('pedidos/new/save', login_required(views.PedidoNewSaveView),
         name='save-pedido'),
    path('carrossel/<int:pk>/del/',
         login_required(views.DelFotoCarroselView), name='foto-del'),
    path('carrossel/new/', login_required(views.AddFotoCarroselView), name='foto-new'),
    path('pedidos/<int:pk>/edit/',
         login_required(views.PedidoEditView), name='pedido-edit'),
]
