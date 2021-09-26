from django.http.response import HttpResponse
from django.shortcuts import render
from MODULOS.Empleados.models import Asistencia
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models import DurationField, F, ExpressionWrapper
from django.utils import timezone
import pytz

# Create your views here.


@login_required
def FicharEntrada(request):
    nuevo_registro=Asistencia(usuario=request.user)
    nuevo_registro.save()
    msj="Hola {}, que tengas un buen día!"
    return HttpResponse(msj.format(request.user))
    

@login_required
def FicharSalida(request):
    fichar_salida=Asistencia.objects.filter(usuario=request.user)[0]
    fichar_salida.hora_salida=timezone.now()
    fichar_salida.save()
    
    data=Asistencia.objects.annotate(cantidad=ExpressionWrapper(F('hora_salida') - F('hora_entrada'), output_field=DurationField())).filter(usuario=request.user)[0]
    fichar_salida.cantidad_horas=data.cantidad
    fichar_salida.save()
    
    return HttpResponse (("Muchas gracias {}, hasta la próxima!").format(request.user))