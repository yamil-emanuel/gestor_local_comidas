from django.db import models
from django.db.models.fields import CharField

from MODULOS.Empleados.models import Empleado
from MODULOS.Cliente.models import Cliente
from MODULOS.Pedidos.models import Pedido


TIPOS_PROBLEMAS=[("FRIA","COMIDA FRIA"),("FM","FALTÓ MERCADERIA"),
                 ("ME","MALA PRESENTACIÓN"),("MD","MUCHA DEMORA"),
                 ("MA","MAL ARMADO DEL PEDIDO")]

class Reclamo(models.Model):
    cliente=models.ForeignKey(Cliente, on_delete=models.CASCADE, default=1)
    pedido=models.ForeignKey(Pedido, on_delete=models.CASCADE)
    observaciones=CharField(choices=TIPOS_PROBLEMAS,max_length=10)
    empleado=models.ForeignKey(Empleado, on_delete=models.CASCADE)
    
    def __str__(self):
        t="{}-{}"
        return t.format(self.pedido,self.observaciones)