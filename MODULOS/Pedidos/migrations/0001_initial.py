# Generated by Django 3.2.6 on 2021-09-24 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Cliente', '0001_initial'),
        ('Empleados', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediosContacto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medio', models.CharField(choices=[('WP', 'WHATSAPP'), ('PY', 'PEDIDOS YA'), ('TE', 'TELEFONO'), ('IG', 'INSTAGRAM'), ('FB', 'FACEBOOK')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='MediosPagos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medio_pago', models.CharField(choices=[('EF', 'EFECTIVO'), ('MP', 'MERCADO PAGO')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='NumeroPedido',
            fields=[
                ('pedido', models.AutoField(primary_key=True, serialize=False)),
                ('hora', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TiposEnvios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_envio', models.CharField(max_length=20)),
                ('precio', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(choices=[('EP', 'EN PREPARACIÓN'), ('LI', 'LISTO P/SER ENTREGADO'), ('EN', 'ENTREGADO')], default='EP', max_length=3)),
                ('entregado', models.DateTimeField(auto_now=True)),
                ('codigoqr', models.ImageField(blank=True, null=True, upload_to='')),
                ('observaciones', models.CharField(max_length=100)),
                ('total', models.IntegerField(blank=True, null=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cliente.cliente')),
                ('medio_contacto', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='medio_contacto', to='Pedidos.medioscontacto')),
                ('medio_pago', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='Pedidos.mediospagos')),
                ('moto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Empleados.empleado')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedido_numero', to='Pedidos.numeropedido')),
                ('tipo_envio', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Pedidos.tiposenvios')),
            ],
            options={
                'ordering': ['-pedido'],
            },
        ),
    ]
