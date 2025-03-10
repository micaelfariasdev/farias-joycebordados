from django.contrib import admin
from .models import Empresa, FotosCarrossel, Cliente, Pedido


class ImagemProdutoInline(admin.TabularInline):
    model = FotosCarrossel
    extra = 1  # Permite adicionar até 3 imagens ao mesmo tempo


class EmpresaAdmin(admin.ModelAdmin):
    inlines = [ImagemProdutoInline]


admin.site.register(Empresa, EmpresaAdmin)


class PedidosInline(admin.TabularInline):
    model = Pedido
    extra = 0
    fields = ('observacao', 'valor_total', 'status', 'pago', 'data_entrega')
    readonly_fields = ('observacao', 'valor_total',  'data_entrega')
    can_delete = False


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    inlines = [PedidosInline]


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    readonly_fields = ('codigo', 'valor_total', )
    list_display = ('codigo', 'cliente', 'data_entrega', 'observacao', 'status', 'pago', 'produto', 'quantidade',
                    'valor', 'valor_total',  'data_update', 'data')
    search_fields = ('cliente', 'produto', 'data')
    ordering = ('status', 'pago')
    list_editable = ('status', 'pago',)
