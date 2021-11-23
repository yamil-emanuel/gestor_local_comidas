# Generated by Django 3.2.6 on 2021-11-22 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Cliente', '0002_calle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='altura',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='calle',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='piso',
        ),
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('altura', models.PositiveBigIntegerField()),
                ('piso', models.CharField(blank=True, max_length=10, null=True)),
                ('lat', models.CharField(blank=True, max_length=15, null=True)),
                ('lon', models.CharField(blank=True, max_length=15, null=True)),
                ('calle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cliente.calle')),
            ],
        ),
        migrations.AddField(
            model_name='cliente',
            name='direccion',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='Cliente.direccion'),
            preserve_default=False,
        ),
    ]
