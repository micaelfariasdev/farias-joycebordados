from django.shortcuts import render
from django.views.generic import DetailView
from .models import Empresa

class ModelDetailView(DetailView):
    model = Empresa
    template_name = ".html"
