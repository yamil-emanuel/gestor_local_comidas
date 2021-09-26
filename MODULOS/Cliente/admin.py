from django.contrib import admin


from MODULOS.Cliente.models import Cliente

# Register your models here.


class ClientesAdmin(admin.ModelAdmin):
    list_display=["id_cliente","calle","altura","piso","nombre","fecha_alta"]
    list_filter=["calle","altura","nombre"]
    
admin.site.register(Cliente,ClientesAdmin)