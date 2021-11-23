from django.db import models

SI_NO=[('S','SI'),('N','NO')]

class Calle(models.Model):
    calle=models.CharField(max_length=50)

    def __str__(self):
        txt="{0}"
        return txt.format(self.calle)
    

class Direccion(models.Model):
    calle=models.ForeignKey(Calle, on_delete=models.CASCADE, null=False, blank=False)
    altura=models.PositiveBigIntegerField()
    piso=models.CharField(max_length=10, blank=True, null=True)
    lat=models.CharField(max_length=15, blank=True, null=True)
    lon=models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        txt="{0} {1} {2}"
        return txt.format(self.calle, self.altura, self.piso)



class Cliente(models.Model):
    id_cliente= models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=15)
    direccion=models.ForeignKey(Direccion, on_delete=models.CASCADE, null=False, blank=False)
    telefono=models.PositiveBigIntegerField()
    es_whatsapp=models.CharField(choices=SI_NO, max_length=2)
    telefono2=models.PositiveBigIntegerField(blank=True, null=True)
    es_whatsapp2=models.CharField(blank=True, null=True, choices=SI_NO, max_length=2)
    categoria=models.CharField(max_length=50, blank=True, null=True)
    fecha_alta=models.DateField(auto_now=True)
    objects=models.Manager()
    
    def __str__(self):
        txt="{0} {1}"
        return txt.format(self.nombre, self.telefono)
    
