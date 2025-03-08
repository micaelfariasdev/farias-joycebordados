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
