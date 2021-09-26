from django.db import models


TAMANO_PRODUCTOS=[("ST","STANDARD"),("CH","CHICO"),("ME","MEDIANO"),("GR","GRANDE")]
TIPOS_PROMOCIONES=[("D","DESCUENTO"),("P","PORCENTAJE")]
        
class CategoriasProductos(models.Model):
    categoria=models.CharField(max_length=20)
    
    def __str__(self):
        txt="{}"
        return txt.format(self.categoria)

class Producto(models.Model):
    id_producto=models.CharField(max_length=20)
    categoria=models.ForeignKey(CategoriasProductos, on_delete=models.CASCADE, default="")
    nombre=models.CharField(max_length=20)
    tamano=models.CharField(choices=TAMANO_PRODUCTOS, max_length=20)
    precio=models.PositiveBigIntegerField()
    
    objects=models.Manager()
    
    def __str__(self):
        txt="{} - {}"
        return txt.format(self.categoria,self.nombre)

class Promocion (models.Model):
    id_promocion=models.CharField(max_length=20)
    tipo_promocion=models.CharField(choices=TIPOS_PROMOCIONES, max_length=2)
    valor_promocion=models.IntegerField(null=True, blank=True)

    objects=models.Manager()
    
    def __str__ (self):
        txt="{}"
        return txt.format(self.id_promocion)