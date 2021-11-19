from django.http.response import HttpResponse
from django.shortcuts import render
from MODULOS.Empleados.models import Asistencia
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models import DurationField, F, ExpressionWrapper
from django.utils import timezone
import pytz
from django.core.paginator import EmptyPage, Paginator

# Create your views here.


@login_required
def FicharEntrada(request):
    #CUANDO SE INGRESA EN DICHA URL, SE CAPTURA LA DATA DEL USUARIO 
    # Y SE ALMACENA EN LA TABLA ASISTENCIA JUNTO CON EL HORARIO DE ENTRADA.
    nuevo_registro=Asistencia(usuario=request.user)
    nuevo_registro.save()
    c={'usuario':request.user}
    return render (request, "fichada.html",c)
    

@login_required
def FicharSalida(request):
    #CUANDO SE INGRESA EN DICHA URL, SE CAPTURA LA DATA DEL USUARIO
    # Y SE ALMACENA EN LA TABLA ASISTENCIA EL HORARIO DE SALIDA. 
    # AUTOMATICAMENTE SE GUARDA EL TIEMPO TRANSCURRIDO ENTRE LA ÚLTIMA ENTRADA Y LA ACTUAL SALIDA
    
    fichar_salida=Asistencia.objects.filter(usuario=request.user)[0]
    fichar_salida.hora_salida=timezone.now()
    fichar_salida.save()
    
    #SE RESTA A LA HORA ACTUAL, LA ÚLTIMA FICHADA DE INGRESO
    data=Asistencia.objects.annotate(cantidad=ExpressionWrapper(F('hora_salida') - F('hora_entrada'), output_field=DurationField())).filter(usuario=request.user)[0]
    fichar_salida.cantidad_horas=data.cantidad
    fichar_salida.save()
    
    c={'usuario':request.user}
    return render (request, "fichada.html",c)

@login_required
def ListadoAsistencias(request):
    
    #QUERYSET BASE
    data=Asistencia.objects.select_related().all()
    #CREAR OBJETO FILTRO (EN TEMPLATE ES UN FORMULARIO GET!!!)
    
    pag = Paginator(data,5)
    
    #SETEAR LA PÁGINA N°1 COMO LA DEFAULT
    page_num=request.GET.get('page',1)
    
    #VERIFICA EL INPUT, SI LA PÁGINA EXISTE, SINO VUELVE A LA PRIMERA
    try:
        page=pag.page(page_num)
    except EmptyPage:
        page=pag.page(1)

    c={'items':page}
    #DEVUELVE EL CONTEXTO (FILTRO DE PEDIDOS)
    
    return render(request,"asistencia.html", c)
    