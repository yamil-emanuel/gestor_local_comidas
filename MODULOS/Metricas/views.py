from django.db import connection
from collections import namedtuple
from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from MODULOS.Pedidos.models import Pedido
from django.db.models import Count, Sum

import matplotlib.pyplot as plt
import base64
from io import BytesIO
from django.utils import timezone 

t = timezone.localtime(timezone.now())

@login_required
def metricas (request):
    
    #-------QUERIES--------#
    
    total_por_mes_y_ano_query="SELECT  strftime('%Y', datetime(hora,'localtime')) as ANO, strftime('%m', datetime(hora,'localtime')) as MES, sum(total) as TOTAL_INGRESOS  from Pedidos_pedido group by ANO,MES;"
    
    total_q_p_por_producto_query="""select Inventario_categoriasproductos.categoria, Inventario_producto.nombre, sum(Carrito_cart.cantidad), sum(Carrito_cart.subtotal)
                                from Pedidos_numeropedido
                                inner join Carrito_cart on Pedidos_numeropedido.pedido = Carrito_cart.pedido_id
                                inner join Inventario_producto on Carrito_cart.producto_id = Inventario_producto.id
                                inner join Inventario_categoriasproductos on Inventario_producto.categoria_id= Inventario_categoriasproductos.id
                                GROUP by categoria,nombre;"""
    
    ingresos_por_dia_query="""SELECT  strftime('%Y', datetime(hora,'localtime')) as ANO, strftime('%m', datetime(hora,'localtime')) as MES, strftime('%d', datetime(hora,'localtime')) as DIA, sum(total) as TOTAL_INGRESOS  from Pedidos_pedido
                        group by ANO,MES, DIA;"""
    
    
    #-------FUNCIONES------#
    def my_custom_sql(query,q):
        #EJECUTA QUERY CUSTOMIZADA, RECIBE QUERY Y "ONE"/"ALL" DEPENDIENDO DE LA CANTIDAD
        #DE ATRIBUTOS QUE SE NECESITE DEVOLVER.
        with connection.cursor() as cursor:
            cursor.execute(query)
            if q == "all":
                data = cursor.fetchall()
            elif q == "one":
                data=cursor.fetchone()
            return data
              
    def get_graph():
        buffer=BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png=buffer.getvalue()
        graph=base64.b64encode(image_png)
        graph=graph.decode('utf-8')
        buffer.close()
        return graph

    def get_plot(x,y,type):
        plt.switch_backend('AGG')
        plt.figure(figsize=(5,3))
        if type=="bar":
            plt.bar(x,y)
        elif type=="plot":
            plt.plot(x,y)
            
        plt.xticks(rotation=45)
        plt.tight_layout()
        graph=get_graph()
        return graph 
       
    total_q_p=my_custom_sql(total_q_p_por_producto_query,"all")
    ingresos_diarios=my_custom_sql(ingresos_por_dia_query,"all")
    
    def grafico_productos():
        x=[(" ").join(x[0:2]) for x in total_q_p]
        y=[y[3] for y in total_q_p]
        chart=get_plot(x,y,"bar")
        return chart
    
    def grafico_ingresos_mes():
        x=[(" ").join(x[0:3]) for x in ingresos_diarios]
        y=[y[3] for y in ingresos_diarios]
        chart=get_plot(x,y,"plot")
        return chart
    
    
    qs= Pedido.objects.filter(hora__year=t.year,
        hora__month=t.month,
            hora__day=t.day)
    
    def OrdenesDelDia():
        return len(qs)
    
    def IngresosDiarios():
        data=(qs.aggregate(Sum('total')))
        return (data["total__sum"])

    def TicketPromedio():
        try:
            qs= Pedido.objects.all()
            total=qs.aggregate(Sum('total'))
            q_pedidos=len(qs)
            return total["total__sum"]/q_pedidos
        except TypeError:
            return 0
    
    def TicketPromedioDiario():
        try:
            data=(qs.aggregate(Sum('total')))
            q=len(qs)
            return data["total__sum"]/q
        except TypeError:
            return 0
    
    def DiferenciaTicketPromedioVsDiario():
        return TicketPromedioDiario()*100/TicketPromedio()

    c={'grafico_productos':grafico_productos(), "grafico_ingresos_mes":grafico_ingresos_mes(),
       'ordenes_del_dia':OrdenesDelDia(), "ingresos_del_dia":IngresosDiarios(),
       'ticket_promedio':TicketPromedio(), "ticket_promedio_dia":TicketPromedioDiario(),
       'diferencia':DiferenciaTicketPromedioVsDiario()}
    
    return render (request, "metr.html", c)
