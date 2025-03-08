from django.contrib import admin
from .models import Empresa, FotosCarrossel

class ImagemProdutoInline(admin.TabularInline):
    model = FotosCarrossel
    extra = 1  # Permite adicionar até 3 imagens ao mesmo tempo

class EmpresaAdmin(admin.ModelAdmin):
    inlines = [ImagemProdutoInline]

admin.site.register(Empresa, EmpresaAdmin)
