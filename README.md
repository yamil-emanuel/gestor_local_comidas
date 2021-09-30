# gestor_local_comidas
#    ANTES DE UTILIZAR: 

PARA UNA COMPLETA EXPERIENCIA COMPLETAR LOCAL_IP Y ALLOWED_HOST EN settings.py Y EJECUTAR EL SERVIDOR PÚBLICAMENTE.
ASÍ SE PODRÁN UTILIZAR LAS FUNCIONALIDADES QR* -> CAMBIAR ESTADO DEL PEDIDO, Marcar entrada y salida, etc .
#   v2.3
*  Se corrigieron cuestiones estéticas. 
*  El carrito ahora dispone de categorías, al clickearlas una lista de todos los productos.
*  El modelo promociones sólo aceptara promociones con valor inferior a 0 (validador)
*  Creación tabla listado de asistencias con paginador.
*  Se integra el formulario de nuevo cliente a una ventana modal en el incio y se elimina la página donde estaba el formulario
*  En el index el botón de cambiar estado, en caso de que el usuario sea un super user te direccionará a un formulario que te hace elegir la moto, en caso de que no fuese así se captura el usuario, se guarda el valor en "moto" y redirecciona a una "mini-comanda"


#   v2.2
*  Se reestructuró la vista del carrito. Ahora cada categoría dispondrá de un botón que activará una ventana modal en la que se podrá seleccionar el ítem + cantidades + observaciones del producto. Una vez agregado el ítem (o promoción). Se redireccionará al carrito correspondiente para continuar con el seguimiento
* Mínimos retoques estéticos como resaltar subtotal/total a lo largo de la operación.

#   v2.1
*  Se reestructuró todo el proyecto. Ahora el mismo se dividirá en las siguientes aplicaciones:

    -Inventario: Almacena data relaionada a los Productos, categorías de productos y promociones. 

    -Cliente: Almacena la data de los clientes y las calles. Sus vistas permiten ingresar un cliente nuevo, ver lista de clientes y ver detalles de cliente.

    -Carrito: Almacena data correspondiente al carrito de productos + carrito de promociones. La vista principal es el carrito, dónde también se puede gestionar (eliminar elementos erróneos)

    -Pedidos: Tablas índices: Numero de pedido, medios de pago, tipo de envío y medio de contacto. La tabla principal almacena info relevante al pedido.
    Las vistas muestran detalles de pedidos, generan pedidos, confirman pedidos, acciones como cambiar el estado de los pedidos, mostrar lista de pedidos y el index.

    -Reclamo: Almacena data relevante a los reclamos. También gestiona la creación de dichos valores.

    -Empleados: Almacena el horario de entrada y salida de los empleados (usuarios), calcula también cuantas horas trabajó dicho empleado.

    -Metricas: Vista métricas.

#   v2.0
*  Se agregó un paginador en lista_pedidos, en la sección de pedidos de detalles_clientes y en la lista de clientes.
*  Se cambió la interfaz del index, en el mismo se agregó una barra de búsqueda que se autocompleta y envía directamente a la sección "nuevo pedido + carrito"

#    v1.9
*  Se creó vista de Métricas, esta muestra los siguientes KPI: ordenes del día, ingresos del día, ticket promedio del día, ticket promedio. Los gráficos son generados automáticamente vía matplotlib cada vez que se visita el sitio Top productos vs Q vendidas(bar) e Ingresos diarios(plot)
*  El dashboard sólo será visible para los superusuarios. Usuarios regulares no tendrán acceso.
*  El estado de los pedidos ahora posee tres opciones EP-> En preparación LI-> LISTO EN->ENTREGADO. Se cambian automáticamente al siguiente estado presionando el botón o utilizando el código QR.
*  Se crea la tabla Reclamos asociada a un pedido y a un empleado. También se agrega un botón a la vista ver pedidos
*  En detalles del cliente se agregó la observación: cantidad de reclamos

#    v1.8
* Se crearon las aplicaciones Empleados y Metricas 
* Empleados: almacena data relevante de los mismos y registra la asistencia (fichada entrada y salida asociada a su usuario), calcula automáticamente el tiempo que estuvo trabajando en la jornada.
* Métricas: Todavía no posee una Interfaz pero ya dispone de kpis (querys)
* Las URLS za se encuentran funcionales pero carecen de UI.

#    v1.7
* Ahora es necesario estar loggueado para poder interactuar en el sitio, caso contrario será enviado a una página de log-in.

#    v1.6
* UI->Se indica cuales son los campos obligatorios y cuales no 
* Se limitaron las consultas en lista_pedidos y lista_clientes a un máximo de 100 observaciones
* Se agregaron ventanas modales cada vez que se sale de una pantalla crítica en el pedido y por ende se elimina data (/cart y /confirmacion)

#    v1.4
* Se pulieron cuestiones estéticas, como por ejemplo: eliminación de subrayados en links, eliminación de celdas extra, etc.
* Filtro por fecha en la lista de pedidos 100% funcional
* Se agregaron cantidades a las promociones
* Se agregó el atributo "estado" al pedido, el cambio del mismo será registrado automáticamente (y actualizado vía lista_pedidos y QR*)
* Se implementó soporta ante la eventual modificación de precios de productos o de valores de las promociones. Ahora se almacenan subvalores dentro de la tabla pedido. Estos son inmutables.