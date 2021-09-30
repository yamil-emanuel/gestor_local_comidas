

from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse


from MODULOS.Carrito.models import Cart, CartPromociones
from MODULOS.Cliente.models import Cliente
from MODULOS.Pedidos.models import NumeroPedido
from MODULOS.Carrito.forms import CartCalzonesForm, CartCanastitasForm, CartForm, CartOtrosForm, CartPizzasForm, CartPromocionesForm, CartEmpanadasForm
from MODULOS.Pedidos.models import Pedido
from MODULOS.Inventario.models import Producto, Promocion


@login_required
def cart(request,id_cliente,pedido):
   #RENDERIZA PÁGINA CON SIGUIENTES FUNCIONES:
   #  BOTON VOLVER: ELIMINA TODOS LOS OBJ CART RELACIONADOS AL PEDIDO + REGRESA A /CLIENTE (SELECCIÓN/INGRESO) DE CLIENTE) 
    #  FORMULARIO PARA INGRESAR OBJETOS EN CART (PROD-CANT)
    #  VISUALIZACIÓN TABLA CON OBJ CART CON EL ID DEL PEDIDO GENERADO ANTERIORMENTE
    #  BOTÓN PARA ELIMINAR CADA UNO DE LOS OBJ CART
    #  VISUALIZACIÓN DE SUBTOTAL CANTIDAD DE ITEMS EN CART Y SUBTOTAL PRECIO
    #  GESTIONA (INGRESA O ELIMINA) ELEMENTOS EN LOS CARRITOS (CART Y CARTPROMOCIONES), INCLUYENDO CANTIDAD*PRECIO.
    #       SI HAY VARIACIÓN FUTURA EN EL PRECIO, NO SE PRODUCIRÁN CAMBIOS EN LAS ESTADÍSTICAS
    
    def subtotal(cart_temp):
        #SUMA TODOS LOS PRECIOS ASOCIADOS A PRODUCTOS EN UN CART ESPECIFICO. 
        #RECIBE cart_temp, TODOS LOS ELEMENTOS CON EL MISMO ID DE PEDIDO
        #LOS VALORES DE LAS PROMOCIONES SON NEGATIVAS.
        
        t=[]
        #POR CADA PRODUCTO.PRECIO QUE CONTIENEN EL MISMO ID DE PEDIDO.
        for producto in cart_temp:
            t.append(producto.subtotal)
            
        for promo in prom_temp:
            t.append(int(promo.subtotal))
        #DEVUELVE LA SUMA
        return sum(t)
    
    def insert_subtotal(id):
        #CALCULA EL SUBTOTAL (CARRITO.CANTIDAD * PRODUCTO.PRECIO) Y LO INSERTA EN LA BASE
        #ESTO SE HACE PARA EVITAR ERRORES DE ESTADÍSTICAS ANTE UN EVENTUAL CAMBIO DE PRECIO.
        data=Cart.objects.get(id=id)
        data.subtotal=(data.producto.precio*data.cantidad)
        data.save()

    def SumarCantidadProductos(cart_temp):
        #DEVUELVE LA CANTIDAD DE PRODUCTOS QUE HAY EN EL CARRITO
        #EJ: EXISTEN 13 ITEMS DE UNO Y 2 DE OTRO. DEVUELVE 15
        t=[]
        for p in cart_temp:
            t.append(p.cantidad)
        return sum(t)
        
    #CLIENTE
    fk_cliente=Cliente.objects.get(id_cliente=id_cliente)
    #PEDIDO
    fk_pedido=NumeroPedido.objects.get(pedido=pedido)
    #CART
    cart_temp=Cart.objects.filter(pedido=pedido).select_related()
    #PROMOCIONES TEMP
    prom_temp=CartPromociones.objects.filter(pedido=pedido)
    
    
    #FORMULARIOS DEL CARRITO (NO RECIBE NULL NI BLANK)
    form_prom=CartPromocionesForm()
    form_emp=CartEmpanadasForm()
    form_pizzas=CartPizzasForm()
    form_calz=CartCalzonesForm()
    form_canast=CartCanastitasForm()
    form_otros=CartOtrosForm()

    
    
    context={'form_prom':form_prom, 'form_emp':form_emp, 'form_pizzas':form_pizzas,
             'form_calz':form_calz, 'form_canast':form_canast, 'form_otros':form_otros,
             "cliente":fk_cliente, 
             "cart_temp":cart_temp,'cantidad_productos':SumarCantidadProductos(cart_temp),
             "subtotal":subtotal(cart_temp),'id_cliente':id_cliente,"pedido":pedido,
             'prom_temp':prom_temp}
    
    
    if request.method=="POST": 
        #SI SE ESTÁ ENVIANDO UN FORMULARIO CON DATA DE CARRITO (PRODUCTO NUEVO - CANTIDAD / PROMOCION- CANTIDAD)
        form_emp=CartForm(request.POST)
        form_pizzas=CartPizzasForm(request.POST)
        form_prom=CartPromocionesForm(request.POST)
      
               
        if form_emp.is_valid():
            
            #SI EL FORMULARIO ES VÁLIDO, SE GUARDA
            final=Cart(producto=form_emp.cleaned_data["producto"], 
                       id_cliente=fk_cliente,
                       pedido=fk_pedido, 
                       observaciones=form_emp.cleaned_data["observaciones"],
                       cantidad=form_emp.cleaned_data["cantidad"]
                       )
            final.save()
            #SE INSERTA EL SUBTOTAL EN CART (SUMA DEL PRECIO DE TODOS LOS ITEMS)
            insert_subtotal(final.pk)

            #REDIRECCIONA A LA PÁGINA CART, ENVÍA DATA CLIENTE, DATA PEDIDO Y EL CONTEXTO:
            # FORM, CLIENTE, CART_TEMP, CANTIDAD DE PRODUCTOS, ID_CLIENTE Y PEDIDO(ID)
            return HttpResponseRedirect(reverse(cart, kwargs={'id_cliente':id_cliente, 'pedido':pedido},),context)

        if form_pizzas.is_valid():
            
            #SI EL FORMULARIO ES VÁLIDO, SE GUARDA
            final=Cart(producto=form_pizzas.cleaned_data["producto"], 
                       id_cliente=fk_cliente,
                       pedido=fk_pedido, 
                       observaciones=form_pizzas.cleaned_data["observaciones"],
                       cantidad=form_pizzas.cleaned_data["cantidad"]
                       )
            final.save()
            #SE INSERTA EL SUBTOTAL EN CART (SUMA DEL PRECIO DE TODOS LOS ITEMS)
            insert_subtotal(final.pk)

            #REDIRECCIONA A LA PÁGINA CART, ENVÍA DATA CLIENTE, DATA PEDIDO Y EL CONTEXTO:
            # FORM, CLIENTE, CART_TEMP, CANTIDAD DE PRODUCTOS, ID_CLIENTE Y PEDIDO(ID)
            return HttpResponseRedirect(reverse(cart, kwargs={'id_cliente':id_cliente, 'pedido':pedido},),context)

        elif form_prom.is_valid():
            
            final=CartPromociones(pedido=fk_pedido,
                                  id_cliente=fk_cliente,
                                  id_promocion=form_prom.cleaned_data["id_promocion"], 
                                  cantidad= form_prom.cleaned_data["cantidad"],
                                  subtotal= int(form_prom.cleaned_data["id_promocion"].valor_promocion)*form_prom.cleaned_data["cantidad"]
                                  )
            final.save()
            
            return HttpResponseRedirect(reverse(cart, kwargs={'id_cliente':id_cliente, 'pedido':pedido},),context)
        
    return render(request, "carrito1.html", context)

@login_required
def EliminarDatosPedido(request,id_cliente,pedido):
    #ELIMINA LOS DATOS RELACIONADOS AL PEDIDO (NO NÚMEROPEDIDO). RECIBE ID_CLIENTE E ID PEDIDO.
    #HORA-PEDIDO-CLIENTE-MEDIO_PAGO-P1-P2-P3-TIPO_ENVIO-TOTAL
    d=Pedido.objects.get(pedido=pedido)
    d.delete()    
    #REGRESAR A CART/ID_CLIENTE/PEDIDO 
    return HttpResponseRedirect(reverse(cart, kwargs={'id_cliente':id_cliente, 'pedido':pedido}))

@login_required
def EliminarPedido(request,pedido):
    #ELIMINA NUMEROPEDIDO + OBJETOS CART, SE ELIMINA RASTRO DE LA OPERACIÓN
    #(REGRESAR A /cart DESDE /cliente )
    data_cart=Cart.objects.filter(pedido=pedido)
    data_cart.delete()
    d=NumeroPedido.objects.get(pk=pedido)
    d.delete()
    #REGRESAR A CLIENTES
    return HttpResponseRedirect(reverse('index'))

@login_required    
def EliminarProductoCart(request,id_cliente,pedido,cart_id):
    #ELIMINA UN PRODUCTO DEL CARRITO, RECIBE id_cliente , pedido (ID) y cart_id 
    #cart_id ES LA CLAVE PRIMARIA DE LA TABLA Cart
    filtro=Cart.objects.get(pk=cart_id)
    filtro.delete()
    
    #REGRESA A CART Y ENVIA COMO CONTEXTO EL id_cliente Y (id) pedido
    return HttpResponseRedirect(reverse(cart, kwargs={'id_cliente':id_cliente, 'pedido':pedido}))

@login_required    
def EliminarPromocionCart(request,id_cliente,pedido,cart_id):
    #ELIMINA UN PRODUCTO DEL CARRITO, RECIBE id_cliente , pedido (ID) y cart_id 
    #cart_id ES LA CLAVE PRIMARIA DE LA TABLA Cart
    filtro=CartPromociones.objects.get(pk=cart_id)
    filtro.delete()
    
    #REGRESA A CART Y ENVIA COMO CONTEXTO EL id_cliente Y (id) pedido
    return HttpResponseRedirect(reverse(cart, kwargs={'id_cliente':id_cliente, 'pedido':pedido}))