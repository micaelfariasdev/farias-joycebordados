# Generated by Django 5.1.7 on 2025-03-08 04:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0003_rename_descricao_empresa_sobre'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='logo'),
        ),
        migrations.AlterField(
            model_name='fotoscarrossel',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fotos_carrossel', to='empresa.empresa'),
        ),
    ]
