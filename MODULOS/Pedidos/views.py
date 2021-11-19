from EL_TREBOL.settings import MEDIA_ROOT, LOCAL_IP, MEDIA_URL
from collections import defaultdict
from django.db import models
from django.db.models.query import QuerySet
from django.http import response
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django import forms
from django.urls import reverse
from django.core.exceptions import MultipleObjectsReturned
from datetime import date
from django.core.files import File
import qrcode
from django.contrib.auth.decorators import login_required
from django.utils import timezone 
from django.core.paginator import EmptyPage, Paginator
from django.http import JsonResponse
from ipware import get_client_ip
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib import messages
from MODULOS.Cliente.forms import ClienteForm,NewUserForm


from MODULOS.Pedidos.models import NumeroPedido
from MODULOS.Cliente.models import Cliente
from MODULOS.Carrito.models import Cart, CartPromociones
from MODULOS.Pedidos.models import Pedido
from MODULOS.Carrito.views import cart
from MODULOS.Reclamo.forms import ReclamosForm
from MODULOS.Reclamo.models import Reclamo
from MODULOS.Cliente.forms import ClienteForm
from .forms import MotoForm, PedidosForm
from .filters import PedidoFilter



t = timezone.localtime(timezone.now())

def buscar_direccion(request):
    #RECIBIR EL MÉTODO GET CÓMO 'direccion'
    direccion=request.GET.get('direccion')
    
    #TUPLA DONDE SE ALMACENARÁN LOS RESULTADOS POR CADA GET 
    # CADA VEZ QUE SE MODIFIQUE EL INPUT SE ENVIARÁ UNA PETICIÓN
    temp=[]
    
    if direccion:
        #SI DIRECCIÓN == TRUE -> FILTRO
        direcciones=Cliente.objects.filter(calle__icontains=direccion)
        
        for dir in direcciones:
            #AGREGAR CADA RESULTADO EN LA TUPLA TEMPORAL
            f=str(dir.id_cliente)+" - "+dir.calle+" "+str(dir.altura)+" "+str(dir.piso)+" ( "+dir.nombre+" ) "
            temp.append(f)
    #DEVOLVER UN JSON AL SCRIPT JS CON LA DATA FILTRADA
    return JsonResponse({'status':200,'data':temp})

@login_required
def show_resume(request,pedido):
    #MUESTRA LA ORDEN DE PEDIDO COMPLETA, INCLUYENDO LAS PROMOCIONES Y LOS PRECIOS FINALES
    # RECIBE ID DEL PEDIDO
    # POSEE UN BOTÓN PARA REGRESAR AL INDEX.
    
    #DATA DEL CARRITO
    carrito=Cart.objects.filter(pedido=pedido).select_related()
    try:
        #POR SI SE GUARDA DOS VECES EL MISMO PEDIDO
        data_pedido=Pedido.objects.select_related().get(pedido=pedido)
    except MultipleObjectsReturned:
        #SE SELECCIONA EL PRIMERO
        data_pedido=Pedido.objects.filter(pedido=pedido).first()
        
    def CrearCodigoQrEntregado(pedido):
        #CREA CÓDIGO QR QUE "MARCA UN PEDIDO COMO ENTREGADO"
        # LO ALMACENA EN PEDIDOS.CODIGOQR
        # CUANDO EL USUARIO ESCANEA EL CÓDIGO, ESTE LO ENVIA A LA FUNCIÓN MARCARCOMOENTREGADO
        
        #URL BASE (FX)
        url="http://{}/marcar_entregado/{}"
        #CREAR CÓDIGO QR
        img = qrcode.make(url.format(LOCAL_IP,pedido))
        #SETEAR EL TIPO DE IMG A EXPORTAR
        type(img)  # qrcode.image.pil.PilImage
        #GUARDAR IMAGEN EN MEDIA_ROOT /PROYECTO/MEDIA
        img.save(MEDIA_ROOT+"{}.png".format(pedido))
        #FORMATEAR EL ACCESO AL ARCHIVO RECIÉN GUARDADO
        f=MEDIA_ROOT+"{}.png".format(pedido)
        #ALMACENAR EL CÓDIGO QR EN LA BASE DE DATOS
        imagen=data_pedido.codigoqr=File(open(f, "rb"))
            
    CrearCodigoQrEntregado(pedido)

    def total_promociones():
        return CartPromociones.objects.filter(pedido=pedido)
    
    context={"data":data_pedido, "carrito":carrito,
             'promociones':total_promociones(),
             "total": data_pedido.total}  

    #DEVUELVE DETALLES DE PEDIDO, CONTEXTO= DATA PEDIDO + CARRITO + DESCUENTOS A APLICAR + TOTAL 
    return render(request,"detalles_pedido.html", context)

@login_required
def nuevo_pedido(request,id_cliente):
    #RECIBE ID_CLIENTE Y GENERA UN NUEVO NÚMERO DE PEDIDO
    pedido=NumeroPedido()
    pedido.save()
    #REDIRIGE A LA SECCIÓN "CARRITO" Y ENVÍA COMO CONTEXTO EL ID DEL CLIENTE Y EL ID DEL PEDIDO 
    return HttpResponseRedirect(reverse(cart, kwargs={'id_cliente':id_cliente, 'pedido':pedido}))

@login_required    
def confirmacion_pedido(request, id_cliente, pedido):
    #MUESTRA VIEW CON UNA LISTA DE ITEMS-CANTIDADES-SUBTOTALES ASOCIADAS AL PEDIDO
    # PERMITE LLENAR EL FORMULARIO CON DATOS COMO TIPO DE ENVIO, PROMOCIONES, ETC. TODOS LOS DATOS SON NECESARIOS
    # EL BOTÓN 'ENVIAR' GENERA UN NUEVO OBJETO EN Pedidos AGREGANDO LA DATA ANTERIORY REDIRECCIONA AL DETALLE DEL PEDIDO
    
    fk_cliente=Cliente.objects.get(id_cliente=id_cliente)
    fk_pedido=NumeroPedido.objects.get(pedido=pedido)
    carrito=Cart.objects.filter(pedido=pedido).select_related()
    promociones=CartPromociones.objects.select_related().filter(pedido=pedido)
    
    
    def calcular_subtotal():
        #SUMA TODOS LOS PRECIOS ASOCIADOS A PRODUCTOS EN UN CART ESPECIFICO. 
        #RECIBE cart_temp, TODOS LOS ELEMENTOS CON EL MISMO ID DE PEDIDO
        t=[]
        #POR CADA PRODUCTO.PRECIO QUE CONTIENEN EL MISMO ID DE PEDIDO.
        for p in carrito:
            t.append(p.subtotal)
            
        for promo in promociones:
            t.append(int(promo.subtotal))
        #DEVUELVE LA SUMA
        return sum(t)
    
    
    #FORMULARIOS
    form=PedidosForm()
    form_nuevo_cliente=ClienteForm()
    context={"form":form,
             "cliente":fk_cliente, "carrito":carrito,
             'id_cliente':id_cliente, "pedido":pedido,
             'promociones':promociones, 'subtotal':calcular_subtotal()}
    
    if request.method=="POST":
        #SI EL USUARIO ENVÍA DATA POR UN FORMULARIO
        
        #OBTENER DATA DEL FORMULARIO
        form=PedidosForm(request.POST)


        if form.is_valid():
            #SI ES VÁLIDO, SE ALMACENA EN Pedidos Y SE PROCEDE A GENERAR
            # DATA RELACIONADA PARA LA CONFIRMACIÓN DEL MISMO
            
            final=Pedido(pedido=fk_pedido, 
                    cliente=fk_cliente, 
                    medio_pago=form.cleaned_data["medio_pago"],
                    tipo_envio=form.cleaned_data["tipo_envio"],
                    medio_contacto=form.cleaned_data["medio_contacto"],
                    paga_con=form.cleaned_data["paga_con"],
                    observaciones=form.cleaned_data["observaciones"])
            final.save()
            
            try:
                #POR SI SE GUARDA DOS VECES EL MISMO PEDIDO
                data_pedido=Pedido.objects.select_related().get(pedido=pedido)
            except MultipleObjectsReturned:
                #SE SELECCIONA EL PRIMERO
                data_pedido=Pedido.objects.filter(pedido=pedido).first()
                

            
            def preciosDeProductos(carrito):
                #SUMA TODOS LOS SUBTOTALES DEL CARRITO (ITEMS CON MISMA ID)
                #SI SE SUMAN LOS PRODUCTO.PRECIO, FRENTE A UN EVENTUAL CAMBIO DE PRECIO
                #SE MODIFICARÍAN TODOS LOS REGISTROS
                precios_productos=[]
                
                #FILTRA EL SUBTOTAL DE CADA ELEMENTO DEL CARRO
                # SE AGREGA EL SUBTOTAL EN UNA LISTA TEMPORAL
                for elemento in carrito:
                    precio=elemento.subtotal
                    precios_productos.append(precio)
                    
                #SE SUMAN TODOS LOS SUBTOTALES Y SE DEVUELVE
                return sum(precios_productos)
            
            def total_promociones():
                promociones_temporal=[]
                for promo in promociones:
                    promociones_temporal.append(promo.id_promocion.valor_promocion*promo.cantidad)
                return sum(promociones_temporal)
                    
               
            def calcular_total(data_pedido):
                """NO TERMINADO, FALTA DESCONTAR LAS PROMOCIONES"""
                #CALCULA Y GUARDA EL TOTAL (PRECIOS PRODUCTOS+PRECIO ENVIO - DESCUENTOS PROMOCIONES)
                
                #ATENCIÓN: LAS PROMOCIONES SE ALMACENAN EN NÚMEROS NEGATIVOS!!!
                
                
                total=preciosDeProductos(carrito)+data_pedido.tipo_envio.precio+total_promociones()
                d=Pedido.objects.get(pedido=pedido)
                d.total=total
                d.save()

            calcular_total(data_pedido)
            
  
            
            
            #REDIRECCIONAR AL DETALLE, ENVIANDO EL ID DEL PEDIDO
            return HttpResponseRedirect(reverse(show_resume, kwargs={'pedido':pedido},),context)
   

    return render(request, "confirmacion.html", context)

@login_required
def MarcarComoEntregado(request,pedido):
    filtro=Pedido.objects.select_related().get(pedido=pedido)
    
    if filtro.estado=="EP":
        filtro.estado="LI"
        filtro.moto=request.user
        msg="{} {} {} - TOTAL : ${}"
        filtro.save()
        return HttpResponse(msg.format(filtro.cliente.calle,
                                       filtro.cliente.altura,
                                       filtro.cliente.piso,
                                       filtro.total))
        
    elif filtro.estado=="LI":
        filtro.estado="EN"
        filtro.save()
    return HttpResponseRedirect(reverse(index))

@login_required
def lista_pedidos(request):
    #DEVUELVE UNA GRILLA CON LA LISTA DE PEDIDOS CON FILTROS
    #PARÁMETRO, DÍA DE LA FECHA

    #QUERYSET BASE
    data=Pedido.objects.all()
    #CREAR OBJETO FILTRO (EN TEMPLATE ES UN FORMULARIO GET!!!)
    
    #CREAR PAGINADOR
    pag = Paginator(data,20)
    
    #SETEAR LA PÁGINA N°1 COMO LA DEFAULT
    page_num=request.GET.get('page',1)
    
    #VERIFICA EL INPUT, SI LA PÁGINA EXISTE, SINO VUELVE A LA PRIMERA
    try:
        page=pag.page(page_num)
    except EmptyPage:
        page=pag.page(1)
        
        
    filtro=PedidoFilter(request.GET, queryset=data)
    #CONVERTIR EL FITRO A QUERYSET Y REESCRIBIR EL QUERYSET INICIAL PARA RENDERIZAR
    data=filtro.qs

    c={'filtro':filtro, 'items':page}
    #DEVUELVE EL CONTEXTO (FILTRO DE PEDIDOS)
    return render(request,"lista_pedidos.html", c)

def login (request,user):
    return render (request, "registration/login.html")

def logout (request):
    return HttpResponseRedirect(reverse(index))

@login_required
@xframe_options_exempt
def seleccionar_moto(request,pedido):
    form_seleccionar_moto=MotoForm()
    c={"form_seleccionar_moto":form_seleccionar_moto}
    
    if request.method=="POST":
        form=MotoForm(request.POST)
        filtro=Pedido.objects.get(pedido=pedido)
        if form.is_valid():
            if filtro.estado=="EP":
                filtro.estado="LI"
                filtro.moto=form.cleaned_data["moto"]
                filtro.save()
                
            elif filtro.estado=="LI":
                filtro.estado="EN"
            filtro.save()
        return HttpResponseRedirect (reverse("index"))
    
    return render (request, "seleccionar_moto.html",c)

@login_required
def index(request):
    """
    INDEX
        -SECCIÓN PEDIDOS DEL DÍA DE LA FECHA
        -BUSCADOR CON FX AUTOCOMPLETADO DE CLIENTES -> GENERA UN PEDIDO NUEVO Y REDIRECCIONA A CARRITO
        -KPI -> PEDIDOS ACTIVOS, LISTOS Y ENTREGADOS DEL DÍA.
    """

    #PEDIDOS DEL DÍA
    pedidos=Pedido.objects.filter(hora__year=t.year, hora__month=t.month, hora__day=t.day)
    
    #KPIs
    activos=len(pedidos.filter(estado="EP"))
    listos=len(pedidos.filter(estado="LI"))
    entregados=len(pedidos.filter(estado="EN"))
    
    #FORMULARIO INICIAR RECLAMO
    form_iniciar_reclamo=ReclamosForm()
    form_nuevo_cliente=ClienteForm()
    
    
    c={'items':pedidos, 'activos':activos, "listos":listos,
    "entregados":entregados, 'form_nuevo_cliente':form_nuevo_cliente}

    if request.method=="POST":
        #numero_pedido=Pedido.objects.get(pedido=pedido)
        """NO FUNCIONA, TIENE QUE RECIBIR EL PEDIDO"""
        form_nuevo_cliente=ClienteForm(request.POST)


        if form_nuevo_cliente.is_valid():
            #SI EL FORMULARIO ES VÁLIDO, SE GUARDA
            nuevo_cliente=form_nuevo_cliente.save()
            #SE REDIRIGE A NUEVO PEDIDO JUNTO AL ID DEL ATRIBUTO GENERADO (ID_CLIENTE)
            return HttpResponseRedirect(reverse('nuevo_pedido', args=(nuevo_cliente.pk,)))
            

    return render(request,"index.html",c)

def register_request(request):
    #VIEW QUE PERMITE A LOS NUEVOS USUARIOS REGRISTRARSE.    
    if request.method == "POST":
        form = NewUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registro completo." )
            return HttpResponseRedirect (reverse('login'))
        else:
            messages.error(request, NewUserForm.error_messages )
    else:
        form = NewUserForm()
    return render (request, "register.html", context={"form":form, 'titulo':"Registrarse"})
