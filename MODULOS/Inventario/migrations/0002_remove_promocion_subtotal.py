# Generated by Django 3.2.6 on 2021-09-24 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promocion',
            name='subtotal',
        ),
    ]