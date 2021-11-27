from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, Paginator
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_exempt


import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.getenv('API_KEY')

from MODULOS.Cliente.models import Cliente, Direccion, Calle
from MODULOS.Pedidos.models import Pedido
from MODULOS.Reclamo.models import Reclamo

from MODULOS.Cliente.forms import DireccionForm, ClienteForm



def DireccionACoordenadas(calle,altura):

    url="https://api.geoapify.com/v1/geocode/search?housenumber={}&street={}&city=Capital%20Federal&state=Buenos%20Aires&country=Argentina&filter=circle:-58.48855661563448,-34.584461706161626,5000&bias=proximity:-58.48857468551239,-34.58450986542681|countrycode:none&format=json&apiKey={}"

    response = requests.get(url.format(calle,altura,API_KEY)).json()
    print(response)
    result=(response['results'][0])
    return (result["lat"], result["lon"])

@login_required
def detalles_cliente(request, id_cliente):
    #DEVUELVE PÁGINA CON CON DATOS RELACIONADOS AL CLIENTE
    # INCLUYENDO CUANTOS PEDIDOS REALIZÓ EL CLIENTE
    # -RESUMEN DE LOS ÚLTIMOS PEDIDOS REALIZADOS POR EL CLIENTE
    # -PAGINADOR (5 PEDIDOS POR PÁGINA)    
    cliente=Cliente.objects.get(id_cliente=id_cliente)
    pedidos=Pedido.objects.filter(cliente=cliente)
    reclamos=Reclamo.objects.filter(cliente=cliente)
    
    def cantidadPedidos(pedidos):
        #DEVUELVE CANTIDAD DE PEDIDOS DEL CLIENTE
        cantidad_pedidos=pedidos.count()
        return cantidad_pedidos
    
    def precioTotalPedidos(pedidos):
        #SUMA LOS TOTALES ($) DE LOS DIFERENTES PEDIDOS DEL CLIENTE
        precios_t=[]
        for pedido in pedidos:
            precios_t.append(pedido.total)
        return sum(precios_t)

    def cantidad_reclamos():
        return len(reclamos)
    
        #CREAR PAGINADOR
    
    pag = Paginator(pedidos,5)
    
    #SETEAR LA PÁGINA N°1 COMO LA DEFAULT
    page_num=request.GET.get('page',1)




    
    #VERIFICA EL INPUT, SI LA PÁGINA EXISTE, SINO VUELVE A LA PRIMERA
    try:
        page=pag.page(page_num)
    except EmptyPage:
        page=pag.page(1)
                
    context={"cliente":cliente, "pedidos":page,
             "precio_total":precioTotalPedidos(pedidos),
             'cantidad_total':cantidadPedidos(pedidos),
             'reclamos':reclamos, 'cantidad_reclamos':cantidad_reclamos()}
    #RENDERIZA
    return render(request,"detalle_cliente.html", context)

@login_required    
def lista_clientes(request):
    #DEVUELVE UNA TABLA CON DATA RELEVANTE DE TODOS LOS CLIENTES
    # TAMBIÉN PERMITE REALIZAR UNA BÚSQUEDA
    
    clientes=Cliente.objects.select_related().all()
    pag = Paginator(clientes,5)
    
    #SETEAR LA PÁGINA N°1 COMO LA DEFAULT
    page_num=request.GET.get('page',1)
    
    #VERIFICA EL INPUT, SI LA PÁGINA EXISTE, SINO VUELVE A LA PRIMERA
    try:
        page=pag.page(page_num)
    except EmptyPage:
        page=pag.page(1)
        
    context={'clientes':page}
    
    if request.method=="POST" or None:
        #SI EL USUARIO MANDA UN FORMULARIO CON DATA (BÚSQUEDA-FILTRO)
        try:
            #SI EL FORMULARIO ENVIA UN TÉRMINO DE BUSQUEDA request.POST['busqueda'], se devuelve este contexto, sino otro
            #SE REALIZA EL FILTRO
            busqueda=request.POST["busqueda"]
            data=Cliente.objects.filter(calle__contains=busqueda)
            context={"clientes":data}

            #SE VUELVE A LA MISMA PÁGINA PERO SE AGREGA LA DATA 'CLIENTES' AL CONTEXTO
            return HttpResponseRedirect(reverse(formularioPedido,context))
        except: 
            pass
    return render(request,"lista_clientes.html", context)    

@xframe_options_exempt
def nueva_direccion(request):
    #ALMACENA UN NUEVO OBJETO DIRECCIÓN (CALLE, ALTURA, PISO, LATITUD, LONGITUD)
    #REDIRECCIONE A NUEVO CLIENTE.

    form=DireccionForm()

    c={'form':form, 'cart':False}

    form=DireccionForm()

    if request.method=="POST":

        form=DireccionForm(request.POST)

        if form.is_valid():
            geodata=DireccionACoordenadas(form.cleaned_data["calle"],form.cleaned_data["altura"])

            data=Direccion(calle=form.cleaned_data["calle"],
                altura=form.cleaned_data["altura"],
                piso=form.cleaned_data["piso"],
                lat=geodata[0],
                lon=geodata[1]
                )
            data.save()

            return HttpResponseRedirect(reverse(nuevo_cliente,kwargs={'direccion':data.pk }))


    return render(request, "f.html", c)

@xframe_options_exempt
def nuevo_cliente(request,direccion):
    #ALMACENA LA DATA RELEVANTE AL USUARIO Y ASOCIA AL MODELO DIRECCIÓN EL CLIENTE
    #REDIRECCIONA A UN NUEVO PEDIDO

    fk_direccion=Direccion.objects.get(pk=direccion)
    c={'form':ClienteForm(), 'cart':True}

    direccion=Direccion.objects.get(pk=direccion)

    if request.method=="POST":

        form=ClienteForm(request.POST)

        if form.is_valid():

            nuevo_cliente=Cliente(nombre=form.cleaned_data["nombre"],
                direccion=fk_direccion,
                telefono=form.cleaned_data["telefono"],
                es_whatsapp=form.cleaned_data["es_whatsapp"],
                telefono2=form.cleaned_data["telefono2"]
                )

            nuevo_cliente.save()




            
            return HttpResponseRedirect(reverse('nuevo_pedido', args=(nuevo_cliente.pk,)))


    return render (request, "f.html", c)


def cargar_calles(request):
    import glob

    PATH="C:/Users/yamil/Desktop/Nueva carpeta/"

    def Cleaner(PATH):
        archivos=glob.glob(PATH+"*")

        for archivo in archivos:
            with open( archivo, mode='r', encoding='utf-8') as file:
                d=file.read()
                d=d.replace("residential","").replace("secondary","").replace("tertiary","").replace("\n","").replace("highway","").replace("name","").replace("footway","").replace("primary","").replace("unclassified","").replace("pedestrian","").replace("track","").replace("motorway","").replace("living_street","").replace("trunk_link","").replace("trunk","").replace("cycleway","").replace("_link","").replace("path","").replace("pedestrian","").replace("service","").replace("platform","")
                d=d.split("\t")
                for calle in d:

                    if Calle.objects.filter(calle=calle).exists():
                        pass
                    else:   
                        data=Calle(calle=calle)
                        data.save()

    Cleaner(PATH)

    return HttpResponse("DONE")