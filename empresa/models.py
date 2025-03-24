
from django.utils.timezone import now
from django.contrib.auth.models import User
import os
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from django.db import models
import qrcode
from pixqrcode import GenerateCode, Pix, PixQrCode
from django.core.files.base import ContentFile
from io import BytesIO


def rename_logo(instance, filename):
    """ Renomeia a imagem para sempre ser 'logo.png' na pasta 'logo/' """
    return os.path.join('logo/', 'logo.png')


class Empresa(models.Model):
    nome = models.CharField(max_length=100)
    logo = models.ImageField(upload_to=rename_logo, null=True, blank=True)
    sobre = models.TextField()
    foto_sobre = models.ImageField(
        upload_to='foto_sobre', null=True, blank=True)
    email = models.EmailField(max_length=100)
    telefone = models.CharField(max_length=15)
    endereco = models.CharField(max_length=100)
    numero = models.CharField(max_length=100)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=9)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if Empresa.objects.exists() and not self.pk:
            raise ValueError("Só pode existir uma empresa no banco de dados!")
        if self.pk:  # Se já existe um objeto salvo
            empresa_antiga = Empresa.objects.get(pk=self.pk)
            if empresa_antiga.logo and self.logo != empresa_antiga.logo:
                if os.path.isfile(empresa_antiga.logo.path):
                    os.remove(empresa_antiga.logo.path)
            if empresa_antiga.foto_sobre and self.foto_sobre != empresa_antiga.foto_sobre:
                if os.path.isfile(empresa_antiga.foto_sobre.path):
                    os.remove(empresa_antiga.foto_sobre.path)
        super().save(*args, **kwargs)


class FotosCarrossel(models.Model):
    empresa = models.ForeignKey(
        Empresa, on_delete=models.CASCADE, related_name="fotos_carrossel")
    foto = models.ImageField(upload_to='fotos_carrossel')

    def __str__(self):
        return self.empresa.nome


@receiver(post_delete, sender=FotosCarrossel)
def delete_foto_carrossel(sender, instance, **kwargs):
    # Deleta a foto do carrossel se existir
    if instance.foto:
        if os.path.isfile(instance.foto.path):
            os.remove(instance.foto.path)


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    numero = models.CharField(max_length=16)

    def save(self, *args, **kwargs):
        newnumber = ''
        for n in self.numero:
            if n.isnumeric():
                newnumber += n

        self.numero = newnumber

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    codigo = models.CharField(
        max_length=5, unique=True, blank=True, null=True)
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, null=True, blank=True)
    empresa = models.ForeignKey(
        Empresa, on_delete=models.CASCADE, null=True, blank=True)
    data = models.DateTimeField(auto_now_add=True)
    data_update = models.DateTimeField(auto_now=True)
    data_entrega = models.DateField(blank=True, null=True)
    produto = models.CharField(max_length=100)
    quantidade = models.IntegerField(null=True, blank=True)
    valor = models.DecimalField(
        max_digits=99, decimal_places=2, null=True, blank=True)
    valor_total = models.DecimalField(
        max_digits=99, decimal_places=2, blank=True, null=True)
    observacao = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100, choices=(
        ('0-pendente', 'Pendente'),
        ('1-producao', 'Produção'),
        ('2-pronto', 'Pronto para entrega'),
        ('3-entregue', 'Finalizado')), blank=True, null=True, default='0-pendente',
    )
    pago = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def gerar_codigo_unico(self):
        import random
        import string
        """Gera um código único para o pedido"""
        while True:
            codigo = random.choices(
                string.ascii_uppercase + string.digits, k=4)
            codigo.append(str(random.randint(0, 9)))
            codigo = ''.join(codigo)
            if not Pedido.objects.filter(codigo=codigo).exists():
                return codigo

    def gerar_qr_pix(self):
        nome = 'Jocileide Fernanda da Silva Farias'
        numero = '86988589907'
        valor = str(int(self.valor_total*100))
        pix = f'({numero[:2]}) {numero[2:]}'
        pix = PixQrCode(nome, pix, "SAO PAULO",
                        valor, f'{self.cliente.nome}{self.codigo}').generate_code()

        # Gerar o QR Code
        qr = qrcode.make(pix)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")

        # Salvar o QR Code no banco de dados como imagem
        self.qr_code.save(f'qr_{self.codigo}.png',
                          ContentFile(buffer.getvalue()), save=False)

        return pix

    def save(self, *args, **kwargs):
        if self.valor is None:
            self.valor = 0
        if self.quantidade is None:
            self.quantidade = 0
        if self.codigo is '':
            self.codigo = self.gerar_codigo_unico()
        if self.valor is not None and self.quantidade is not None:

            self.valor_total = self.valor * self.quantidade
        else:
            self.valor_total = 0

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.codigo


class HistoricoPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido, on_delete=models.CASCADE, related_name="historico")
    alteracoes = models.JSONField()  # Guarda as mudanças feitas
    data_alteracao = models.DateTimeField(default=now)
