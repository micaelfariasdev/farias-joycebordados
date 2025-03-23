
from django.contrib.auth.decorators import login_required
from .. import views
from django.urls import path

app_name = 'adm'

urlpatterns = [
    path('profile/carrossel/',
         login_required(views.CarrosselProfileView), name='carrossel'),
    path('profile/carrossel/new/',
         login_required(views.AddFotoCarroselView), name='foto-new'),
    path('profile/carrossel/<int:pk>/del/',
         login_required(views.DelFotoCarroselView), name='foto-del'),
]
