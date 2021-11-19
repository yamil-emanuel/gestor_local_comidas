from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, Paginator
from django.urls import reverse


from MODULOS.Cliente.models import Cliente
from MODULOS.Pedidos.models import Pedido
from MODULOS.Reclamo.models import Reclamo




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

