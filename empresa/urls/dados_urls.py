
from django.contrib.auth.decorators import login_required
from .. import views
from django.urls import path

app_name = 'adm'

urlpatterns = [
    path('profile/config/', login_required(views.DadosProfileView), name='dados'),
    path('profile/config/edit/',
         login_required(views.DadosEditView), name='dados-edit'),
]
