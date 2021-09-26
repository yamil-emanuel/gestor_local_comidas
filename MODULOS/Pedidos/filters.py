import django_filters

from django_filters import DateRangeFilter,DateFilter
from django.forms.widgets import DateInput, SelectDateWidget
from datetime import datetime
from django.utils import timezone

from .models import Pedido
from django.utils import timezone 

t = timezone.localtime(timezone.now()).date()



class PedidoFilter(django_filters.FilterSet):
    filtro=("-").join([str(t.day),str(t.month),str(t.year)])
    print(filtro)
    #SOLO MUESTRA FILTROS DEBAJO DESCRITOS. 
    fecha_comienzo =DateFilter(widget=DateInput(attrs={'type': 'date'}),
                               label="Fecha inicio ",lookup_expr="gte",field_name="hora",
                               initial=filtro)
    

    fecha_final=DateFilter(widget=DateInput(attrs={'type': 'date'}),
                           label="Fecha final ",lookup_expr="lte",field_name="hora")


    
    class Meta:
        model=Pedido
        #NO MUESTRA FILTROS POR FUERA DE LOS DESCRITOS EN LA CLASE ARRIBA.
        fields=""


