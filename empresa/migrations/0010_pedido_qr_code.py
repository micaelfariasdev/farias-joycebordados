# Generated by Django 5.1.7 on 2025-03-13 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0009_pedido_data_update_alter_pedido_codigo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='qr_codes/'),
        ),
    ]
