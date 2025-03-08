from django.urls import path
from .views import HomeView

app_name = 'joycebordados'

urlpatterns = [
    path('', HomeView, name='home'),
]
