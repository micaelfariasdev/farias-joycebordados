from django.urls import path
from .views import HomeView, red

app_name = 'joycebordados'

urlpatterns = [
    path('', HomeView, name='home'),
    path('<str:cod>', red, name='red'),
]
