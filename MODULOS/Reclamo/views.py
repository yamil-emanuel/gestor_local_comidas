from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import EmptyPage, Paginator


from MODULOS.Reclamo.forms import ReclamosForm
from MODULOS.Reclamo.models import Reclamo
from MODULOS.Pedidos.models import Pedido
from django.views.decorators.clickjacking import xframe_options_exempt

@login_required
@xframe_options_exempt
def iniciar_reclamo(request,pedido):
    #FORMULARIO
    form=ReclamosForm()
    #BUSCAR DATA RELEVANTE AL PEDIDO
    data=Pedido.objects.select_related().get(pedido=pedido)
    
    context={"form":form}
    
    if request.method=="POST": 
        #SI SE ESTÁ ENVIANDO UN FORMULARIO CON LAS OBSERVACIONES Y EL EMPLEADO
        form=ReclamosForm(request.POST)
        
        if form.is_valid():
            #SI EL FORMULARIO ES VÁLIDO, SE GUARDA
            final=Reclamo(pedido=data, 
                           cliente=data.cliente,
                           observaciones=form.cleaned_data["observaciones"],
                           empleado=form.cleaned_data["empleado"])
            final.save()
            
            return HttpResponseRedirect (reverse("index"))
    

    return render (request, "iniciar_reclamo.html", context)

@login_required

def ver_reclamos(request):
    #DEVUELVE UNA GRILLA CON LA LISTA DE RECLAMOS CON FILTROS
    #PARÁMETRO, DÍA DE LA FECHA

    #QUERYSET BASE
    data=Reclamo.objects.all()
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
        

    c={'items':page}
    #DEVUELVE EL CONTEXTO (FILTRO DE PEDIDOS)
    return render(request,"lista_reclamos.html", c)
