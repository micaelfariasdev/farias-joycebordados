
from .views import ModelDetailView
from django.urls import path

name_app = 'empresa'

urlpatterns = [
    path('', ModelDetailView.as_view(), name='empresa'),
]
