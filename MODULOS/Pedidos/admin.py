from django.contrib import admin


from MODULOS.Pedidos.models import MediosPagos,  NumeroPedido, TiposEnvios, MediosContacto, Pedido

    
class PedidosAdmin(admin.ModelAdmin):
    list_display=["hora","pedido","cliente","medio_pago","total"]
    list_filter=["pedido","hora"]
    

admin.site.register(Pedido,PedidosAdmin)

admin.site.register(MediosPagos)
admin.site.register(NumeroPedido)
admin.site.register(TiposEnvios)
admin.site.register(MediosContacto)
