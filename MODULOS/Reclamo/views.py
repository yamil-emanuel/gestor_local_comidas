from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

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
