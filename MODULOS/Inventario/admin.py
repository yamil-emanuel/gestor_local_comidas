from django.contrib import admin
from MODULOS.Inventario.models import CategoriasProductos, Producto, Promocion

# Register your models here.



class ProductosAdmin(admin.ModelAdmin):
    list_display=['id_producto','categoria','nombre','precio']
    list_filter=['categoria']

admin.site.register(Producto, ProductosAdmin)
admin.site.register(CategoriasProductos)
admin.site.register(Promocion)