from django.db import models
from django.conf import settings
from django.db.models.fields import AutoField, IntegerField
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Turnos (models.Model):
    turno=models.CharField(max_length=7)
    horario_inicio=models.PositiveIntegerField()
    horario_finalizacion=models.PositiveIntegerField()
    
    def __str__ (self):
        t="{}"
        return t.format(self.turno)

class Empleado(models.Model):
    nombre=models.CharField(max_length=25)
    apellido=models.CharField(max_length=25)
    telefono=models.PositiveIntegerField()
    sector=models.CharField(max_length=10)
    turno=models.ForeignKey(Turnos, on_delete=models.CASCADE)
    
    def __str__(self):
        t="{}"
        return t.format(self.nombre)


class Asistencia(models.Model):
    usuario= models.ForeignKey(User, blank=True, null=True,editable=False, on_delete=models.CASCADE,)
    hora_entrada=models.DateTimeField(auto_now_add=True)
    hora_salida=models.DateTimeField(auto_now_add=True, blank=True, null=True)
    cantidad_horas=models.CharField(blank=True, null=True, max_length=30)
    class Meta:
        ordering = ['-hora_entrada']

    def __str__(self):
        t="{} {}"
        return t.format(self.usuario, self.hora_entrada)