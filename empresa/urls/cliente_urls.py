
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .. import views
from django.urls import path

app_name = 'adm'

urlpatterns = [
    path('profile/clientes/', login_required(views.ClientesListView), name='clientes'),
    path('profile/clientes/<int:pk>/', login_required(views.EditCliente), name='cliente-edit'),
]
