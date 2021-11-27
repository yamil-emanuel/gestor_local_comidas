"""EL_TREBOL URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django import contrib
from django import urls
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from django.urls.conf import include


from MODULOS.Metricas.views import metricas, maps
from MODULOS.Pedidos.views import buscar_direccion, seleccionar_moto, show_resume, nuevo_pedido, confirmacion_pedido, MarcarComoEntregado, lista_pedidos, login, logout, index, register_request
from MODULOS.Carrito.views import cart, EliminarDatosPedido, EliminarPedido, EliminarProductoCart, EliminarPromocionCart, form
from MODULOS.Cliente.views import detalles_cliente, lista_clientes, nueva_direccion, nuevo_cliente, cargar_calles
from MODULOS.Empleados.views import FicharEntrada, FicharSalida, ListadoAsistencias
from MODULOS.Reclamo.views import iniciar_reclamo, ver_reclamos


urlpatterns = [
    #ADMIN
    path('admin/', admin.site.urls),
    
    #ACCOUNTS -DJANGO -LOG IN - LOG OUT.
    path("accounts/", include ('django.contrib.auth.urls')),
    path('login/', LoginView.as_view(template_name="login.html"), name="login"),
    path('logout/', LogoutView.as_view(template_name="logout.html"), name="logout"),
    path("register/", register_request, name="register"),

    
    #METRICAS
    path('metricas/',metricas, name="metricas"),
    path('maps/', maps, name="maps"),
    
    #INDEX
    path('index/', index, name="index"),
    url('index/', index, name="index"),
    
    #BUSQUEDA DE DIRECCIÓN EN INDEX
    path('busquedacliente/',buscar_direccion),
    
    #MUESTRA RESUMEN DE LA OPERACIÓN
    path('show_resume/<int:pedido>',show_resume, name="show_resume"),
    url('show_resume/<int:pedido>',show_resume, name="show"),
    
    #CONFIRMA LA OPERACIÓN SE CREA OBJ PEDIDO (PROMOCIONES-PRECIO ENVÍO-MEDIO DE PAGO-ETC)
    path('confirmacion/<int:id_cliente>/<int:pedido>',confirmacion_pedido, name="confirmacion_pedido"),
    url('confirmacion/<int:id_cliente>/<int:pedido>', confirmacion_pedido, name="confirmacion"),
    
    #CARRITO, RECIBE ID_CLIENTE Y N DE PEDIDO
    path('cart/<int:id_cliente>/<int:pedido>',cart, name="cart"),
    url('cart/<int:id_cliente>/<int:pedido>',cart, name="cart_url"),
    path('cart/seleccionar_producto/<int:id_cliente>/<int:pedido>/<int:categoria>', form, name="seleccionar_producto"),
    url('cart/seleccionar_producto/<int:id_cliente>/<int:pedido>/<int:categoria>', form, name="seleccionar_producto_url"),

     
    #CREA UN NUEVO N DE PEDIO Y REDIRECCIONA AL CARRITO (CON EL ID_USUARIO Y N PEDIDO)
    path('nuevo_pedido/<int:id_cliente>',nuevo_pedido, name="nuevo_pedido"),
    url('nuevo_pedido/<int:id_cliente>',nuevo_pedido, name="nuevo_pedido"),
    
    #ELIMINA OBJ DEL CARRITO. RECIBE ID_CLIENTE N DE PEDIDO E cart_id (PK DEL OBJ EN CART)
    path('eliminar_cart_element/<int:id_cliente>/<int:pedido>/<int:cart_id>', EliminarProductoCart, name="eliminar_cart_id"),
    url('eliminar_cart_element/<int:id_cliente>/<int:pedido>/<int:cart_id>', EliminarProductoCart, name="eliminar_cart_"),
    path('eliminar_promocion_cart/<int:id_cliente>/<int:pedido>/<int:cart_id>',EliminarPromocionCart, name="eliminar_promocion_cart_id"),
    url('eliminar_promocion_cart/<int:id_cliente>/<int:pedido>/<int:cart_id>',EliminarPromocionCart, name="eliminar_promocion_cart_id"),
        
        
    #ELIMINA OBJ DE PEDIDOS (MEDIO DE PAGO-PROMOCIONES-ENVIO-ETC)
    path('eliminar_datos_pedido/<int:id_cliente>/<int:pedido>',EliminarDatosPedido, name="eliminar_datos_pedido"),
    url('eliminar_datos_pedido/<int:id_cliente>/<int:pedido>',EliminarDatosPedido, name="eliminar_datos_pedido"),
    
    #MARCAR UN PEDIDO COMO ENTREGADO ('F')
    path('marcar_entregado/<int:pedido>', MarcarComoEntregado, name="marcar_entregado"),
    url('marcar_entregado/<int:pedido>', MarcarComoEntregado, name="marcar_entregado"),
    path('seleccionar_moto/<int:pedido>', seleccionar_moto, name="seleccionar_moto"),
    url('seleccionar_moto/<int:pedido>', seleccionar_moto, name="seleccionar_moto"),
    
    #ELIMINAR N DE PEDIDO, REDIRECCIONA A /CLIENTE
    path('eliminar_pedido/<int:pedido>',EliminarPedido, name="eliminar_pedido"),
    url('eliminar_pedido/<int:pedido>',EliminarPedido, name="eliminar_pedido_url"),
    
    #INICIAR RECLAMO
    path('iniciar_reclamo/<int:pedido>', iniciar_reclamo, name="iniciar_reclamo"),
    url('iniciar_reclamo/<int:pedido>', iniciar_reclamo, name="iniciar_reclamo_url"),
    url('lista_reclamos/', ver_reclamos, name="lista_reclamos_url"),


    #MUESTRA UNA LISTA DE PEDIDOS FILTRADA POR DISTINTOS VALORES
    path('lista_pedidos/', lista_pedidos, name="lista_pedidos"),
    url('lista_pedidos/', lista_pedidos, name="lista_pedidos_url"),

    #MUESTRA DETALLES DEL CLIENTE (RECIBE ID_CLIENTE)
    path('cliente_detalles/<int:id_cliente>/', detalles_cliente, name="detalles_cliente"),
    url('cliente_detalles/<int:id_cliente>/', detalles_cliente, name="detalles_cliente"),
    
    #MUESTRA UNA LISTA CON TODOS LOS CLIENTES
    path('nueva_direccion/', nueva_direccion, name="nueva_direccion"),
    path('nuevo_cliente/<int:direccion>/', nuevo_cliente, name="nuevo_cliente"),
    path('clientes_lista/', lista_clientes, name="lista_clientes"),
    
    #FICHAR ENTRADA
    path('fichar_entrada/', FicharEntrada, name="fichar_entrada"),
    path('fichar_salida/', FicharSalida, name="fichar_salida" ),
    path('asistencia/', ListadoAsistencias, name="lista_asistencias"),
    url('asistencia/', ListadoAsistencias, name="lista_asistencias"),

    #CARGAR OBJETOS
    path("cargar_calles/", cargar_calles, name="cargar_calles"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
