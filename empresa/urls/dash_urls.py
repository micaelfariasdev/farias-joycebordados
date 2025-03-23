
from django.contrib.auth.decorators import login_required
from .. import views
from django.urls import path

app_name = 'adm'

urlpatterns = [
    path('profile/dash/', login_required(views.DashBoardView), name='empresa'),
]
