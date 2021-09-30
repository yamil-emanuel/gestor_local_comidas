# Generated by Django 3.2.6 on 2021-09-30 16:28

import MODULOS.Inventario.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0003_alter_promocion_valor_promocion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promocion',
            name='valor_promocion',
            field=models.IntegerField(default=0, validators=[MODULOS.Inventario.validators.ValorPromocionValidador]),
            preserve_default=False,
        ),
    ]
