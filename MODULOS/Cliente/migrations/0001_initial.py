# Generated by Django 3.2.6 on 2021-09-24 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id_cliente', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=15)),
                ('calle', models.CharField(max_length=50)),
                ('altura', models.PositiveBigIntegerField()),
                ('piso', models.CharField(blank=True, max_length=10, null=True)),
                ('telefono', models.PositiveBigIntegerField()),
                ('es_whatsapp', models.CharField(choices=[('S', 'SI'), ('N', 'NO')], max_length=2)),
                ('telefono2', models.PositiveBigIntegerField(blank=True, null=True)),
                ('es_whatsapp2', models.CharField(blank=True, choices=[('S', 'SI'), ('N', 'NO')], max_length=2, null=True)),
                ('categoria', models.CharField(blank=True, max_length=50, null=True)),
                ('fecha_alta', models.DateField(auto_now=True)),
            ],
        ),
    ]
