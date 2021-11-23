from django.contrib import admin


from MODULOS.Cliente.models import Cliente, Direccion, Calle

# Register your models here.


class ClientesAdmin(admin.ModelAdmin):
    list_display=["id_cliente","direccion","nombre","fecha_alta"]
    list_filter=["direccion","nombre"]
    
admin.site.register(Cliente,ClientesAdmin)
admin.site.register(Direccion)
admin.site.register(Calle)
