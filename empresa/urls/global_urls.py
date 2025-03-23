
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .. import views
from django.urls import path

app_name = 'adm'

urlpatterns = [
    path('profile/login/', views.Login, name='login'),
    path('profile/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/fechar/', login_required(views.fechar_pagina), name='fechar_pagina'),
    path('profile/send/<int:pk>', login_required(views.whastapp), name='sendwht'),
]
