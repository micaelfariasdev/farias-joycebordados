import os
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.db import models


class Empresa(models.Model):
    nome = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logo', null=True, blank=True)
    sobre = models.TextField()
    foto_sobre = models.ImageField(
        upload_to='foto_sobre', null=True, blank=True)
    email = models.EmailField(max_length=100)
    telefone = models.CharField(max_length=15)
    endereco = models.CharField(max_length=100)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=9)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if Empresa.objects.exists() and not self.pk:
            raise ValueError("Só pode existir uma empresa no banco de dados!")
        super().save(*args, **kwargs)


class FotosCarrossel(models.Model):
    empresa = models.ForeignKey(
        Empresa, on_delete=models.CASCADE, related_name="fotos_carrossel")
    foto = models.ImageField(upload_to='fotos_carrossel')

    def __str__(self):
        return self.empresa.nome


# Função para excluir imagens ao deletar


@receiver(post_delete, sender=Empresa)
def delete_empresa_images(sender, instance, **kwargs):
    # Deleta o logo se existir
    if instance.logo:
        if os.path.isfile(instance.logo.path):
            os.remove(instance.logo.path)

    # Deleta a foto_sobre se existir
    if instance.foto_sobre:
        if os.path.isfile(instance.foto_sobre.path):
            os.remove(instance.foto_sobre.path)


@receiver(post_delete, sender=FotosCarrossel)
def delete_foto_carrossel(sender, instance, **kwargs):
    # Deleta a foto do carrossel se existir
    if instance.foto:
        if os.path.isfile(instance.foto.path):
            os.remove(instance.foto.path)


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    numero = models.CharField(max_length=15)

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    codigo = models.CharField(
        max_length=5, unique=True, blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    data_update = models.DateTimeField(auto_now=True)
    data_entrega = models.DateField(blank=True, null=True)
    produto = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    observacao = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100, choices=(
        ('0-pendente', 'Pendente'),
        ('1-producao', 'Produção'),
        ('2-pronto', 'Pronto para entrega'),
        ('3-entregue', 'Finalizado')), blank=True, null=True, default='0-pendente',
    )
    pago = models.BooleanField(default=False)

    def gerar_codigo_unico(self):
        import random
        import string
        """Gera um código único para o pedido"""
        while True:
            codigo = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=5))
            if not Pedido.objects.filter(codigo=codigo).exists():
                return codigo

    def save(self, *args, **kwargs):
        if self.codigo is None:
            self.codigo = self.gerar_codigo_unico()
        if self.valor is not None and self.quantidade is not None:
            self.valor_total = self.valor * self.quantidade
        else:
            self.valor_total = 0
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.codigo


from empresa.models import Pedido
from datetime import timedelta
from django.utils.timezone import now




