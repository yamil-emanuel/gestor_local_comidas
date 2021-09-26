from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, Paginator
from django.urls import reverse

from MODULOS.Cliente.models import Cliente
from MODULOS.Pedidos.models import Pedido
from MODULOS.Reclamo.models import Reclamo
from MODULOS.Cliente.forms import ClienteForm




@login_required
def formularioPedido (request):
    #GENERA VIEW CON UNA CAJA DE BÚSQUEDA QUE FILTRA CLIENTES UTILIZANDO LA CALLE UTILIZADA
    # UNA VEZ REALIZADA LA BÚSQUEDA(FILTRO), SE PUEDE SELECCIONAR UN CLIENTE DE LA LISTA
    # PERMITE GUARDAR UN NUEVO CLIENTE A TRAVÉS DE FORMULARIO
    #EL BOTÓN VOLVER TE DEVUELVE AL INICIO
    
    data=Cliente.objects.all()[:50]
    #GENERAR FORMULARIO PARA CLIENTE:
    form=ClienteForm()
    context={'form':form} 
    
    
    if request.method=="POST":
        #SI EL USUARIO MANDA UN FORMULARIO CON DATA
        try:
            #SI EL FORMULARIO ENVIA UN TÉRMINO DE BUSQUEDA request.POST['busqueda'], se devuelve este contexto, sino otro
            #SE REALIZA EL FILTRO
            busqueda=request.POST["busqueda"]
            data=Cliente.objects.filter(calle__contains=busqueda)
            context={"form":form,"clientes":data}

            #SE VUELVE A LA MISMA PÁGINA PERO SE AGREGA LA DATA 'CLIENTES' AL CONTEXTO
            return HttpResponseRedirect(reverse(formularioPedido,context))
        
        #SI EL FORMULARIO CONTIENE LA DATA CORRESPONDIENTE A UN NUEVO USUARIO
        except: 
            form=ClienteForm(request.POST)
            if form.is_valid():
                #SI EL FORMULARIO ES VÁLIDO, SE GUARDA
                nuevo_cliente=form.save()
                #SE REDIRIGE A NUEVO PEDIDO JUNTO AL ID DEL ATRIBUTO GENERADO (ID_CLIENTE)
                return HttpResponseRedirect(reverse('nuevo_pedido', args=(nuevo_cliente.pk,)))
    
    #SE RENDERIZA CON CONTEXT=FORMULARIO
    return render(request, "clientes.html", context)

@login_required
def detalles_cliente(request, id_cliente):
    #DEVUELVE PÁGINA CON CON DATOS RELACIONADOS AL CLIENTE
    # INCLUYENDO CUANTOS PEDIDOS REALIZÓ EL CLIENTE
    # -RESUMEN DE LOS ÚLTIMOS PEDIDOS REALIZADOS POR EL CLIENTE
    
    
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
    
    clientes=Cliente.objects.all()
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

