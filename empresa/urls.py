
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path

app_name = 'adm'

urlpatterns = [
    path('profile/login/', views.Login, name='login'),
    path('profile/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/dash/', login_required(views.DashBoardView), name='empresa'),
    path('profile/config/', login_required(views.DadosProfileView), name='dados'),
    path('profile/config/edit/',
         login_required(views.DadosEditView), name='dados-edit'),
    path('profile/carrossel/',
         login_required(views.CarrosselProfileView), name='carrossel'),
    path('profile/pedidos/', login_required(views.PedidosListView), name='pedidos'),
    path('profile/pedidos/new/', login_required(views.PedidoNewView),
         name='new-pedido'),
    path('profile/pedidos/new/save', login_required(views.PedidoNewSaveView),
         name='save-pedido'),
    path('profile/carrossel/new/',
         login_required(views.AddFotoCarroselView), name='foto-new'),
    path('profile/pedidos/api/',
         login_required(views.pedidos_json), name='pedido-api'),
    path('profile/fechar/', login_required(views.fechar_pagina), name='fechar_pagina'),
    path('profile/clientes/new', login_required(views.NewCliente), name='cliente-new'),
    path('profile/pedidos/<int:pk>/', login_required(views.PedidodetailView),
         name='detail-pedido'),
    path('profile/pedidos/<int:pk>/edit/',
         login_required(views.PedidoEditView), name='pedido-edit'),
    path('profile/pedidos/<int:pk>/del/',
         login_required(views.PedidoDelView), name='pedido-del'),
    path('profile/carrossel/<int:pk>/del/',
         login_required(views.DelFotoCarroselView), name='foto-del'),
    path('profile/send/<int:pk>', login_required(views.whastapp), name='sendwht'),

]
