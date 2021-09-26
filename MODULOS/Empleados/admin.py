from MODULOS.Empleados.models import Asistencia, Empleado, Turnos
from django.contrib import admin

# Register your models here.
class AsistenciaAdmin(admin.ModelAdmin):
    actions = None
    list_display=["usuario","hora_entrada","hora_salida","cantidad_horas"]
    def save_model(self, request, obj, form, change):
        if not obj.usuario:
            obj.usuario = request.user
        obj.save()
    
    

admin.site.register(Empleado)
admin.site.register(Turnos)
admin.site.register(Asistencia, AsistenciaAdmin)