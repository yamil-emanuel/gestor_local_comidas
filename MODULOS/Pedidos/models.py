from django.db import models
from django.db.models.aggregates import Max
from django.db.models.enums import Choices
from django.db.models.fields import CharField, DateField, IntegerField
from django.db.models.fields import related
from django.db.models.fields.related import ForeignKey
from django import forms
from django.contrib.auth.models import User

from MODULOS.Empleados.models import Empleado
from MODULOS.Cliente.models import Cliente
from MODULOS.Empleados.models import Empleado


MEDIO_CONTACTO=[('WP','WHATSAPP'),('PY','PEDIDOS YA'),('TE','TELEFONO'),('IG','INSTAGRAM'),('FB','FACEBOOK')]

DESCUENTOS=[('PRECIO',"PRECIO"),('DESCUENTO','DESCUENTO')]

ESTADOS=[("EP","EN PREPARACIÓN"),("LI","LISTO P/SER ENTREGADO"),("EN","ENTREGADO")]
MEDIOS_PAGO=[("EF","EFECTIVO"),("MP","MERCADO PAGO")]


                
class MediosPagos(models.Model):
    medio_pago=models.CharField(max_length=3, choices=MEDIOS_PAGO)
    
    def __str__(self):
        t="{}"
        return t.format(self.medio_pago)

class NumeroPedido(models.Model):
    pedido=models.AutoField(primary_key=True)
    hora=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        t="{}"
        return t.format(self.pedido)

class TiposEnvios(models.Model):
    tipo_envio=models.CharField(max_length=20)
    precio=models.IntegerField()   
    def __str__(self):
        t="{}"
        return t.format(self.tipo_envio)

class MediosContacto(models.Model):
    medio=models.CharField(max_length=20, choices=MEDIO_CONTACTO)
    
    def __str__(self):
        t="{}"
        return t.format(self.medio)

class Pedido(models.Model):
    
    hora=models.DateTimeField(auto_now_add=True)
    pedido=models.ForeignKey(NumeroPedido, on_delete=models.CASCADE, null=False, blank=False, related_name="pedido_numero")
    cliente=models.ForeignKey(Cliente, on_delete=models.CASCADE, null=False, blank=False)
    medio_pago=models.ForeignKey(MediosPagos, on_delete=models.CASCADE, null=True, blank=True, default=1)
    medio_contacto=models.ForeignKey(MediosContacto, on_delete=models.CASCADE, blank=False, null=False, related_name="medio_contacto", default=1)
    tipo_envio=models.ForeignKey(TiposEnvios, on_delete=models.CASCADE, default=1)
    estado=models.CharField(max_length=3, choices=ESTADOS, default="EP")
    entregado=models.DateTimeField(auto_now=True)
    moto=models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    codigoqr=models.ImageField(upload_to="" , null=True, blank=True)  
    observaciones=CharField(max_length=100)
    paga_con=IntegerField(null=True, blank=True)
    total=models.IntegerField(null=True, blank=True)
    class Meta:
        ordering = ['-pedido']
    
    def __str__(self):
        t="{}"
        return t.format(self.pedido)
    
