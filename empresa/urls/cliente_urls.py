
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .. import views
from django.urls import path

app_name = 'adm'

urlpatterns = [
    path('profile/clientes/new', login_required(views.NewCliente), name='cliente-new'),
]
