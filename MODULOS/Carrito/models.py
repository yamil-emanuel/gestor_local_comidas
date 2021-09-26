from django.db import models

from MODULOS.Cliente.models import Cliente
from MODULOS.Inventario.models import Producto
from MODULOS.Pedidos.models import NumeroPedido, Pedido
from MODULOS.Inventario.models import Promocion

class Cart(models.Model):
    pedido=models.ForeignKey(NumeroPedido, on_delete=models.CASCADE, null=False, blank=False)
    id_cliente=models.ForeignKey(Cliente, on_delete=models.CASCADE, null=False, blank=False)
    producto=models.ForeignKey(Producto, on_delete=models.CASCADE,null=False, blank=False)
    cantidad=models.PositiveIntegerField()
    subtotal=models.PositiveIntegerField(null=True, blank=True)
    observaciones=models.CharField(max_length=100, null=True, blank=True)


    objects=models.Manager()
    
    def __str__(self):
        t="{} - {} - {}"
        return t.format(self.pedido, self.producto, self.cantidad)

class CartPromociones(models.Model):
    pedido=models.ForeignKey(NumeroPedido, on_delete=models.CASCADE, null=False, blank=False)
    id_cliente=models.ForeignKey(Cliente, on_delete=models.CASCADE, null=False, blank=False)
    id_promocion=models.ForeignKey(Promocion, on_delete=models.CASCADE, null=True, blank=True)
    cantidad=models.PositiveIntegerField()
    subtotal=models.IntegerField(null=True, blank=True)
    
    objects=models.Manager()
    
    def __str__(self):
        t="{}"
        return t.format(self.id)