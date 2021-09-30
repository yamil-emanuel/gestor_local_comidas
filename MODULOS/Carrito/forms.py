from MODULOS.Cliente.views import lista_clientes
from django.db.models import fields

from django.db.models.base import Model
from django import forms
from django.forms import ModelForm, ModelChoiceField
from .models import Cart, CartPromociones
from MODULOS.Inventario.models import Producto,Promocion

class CartForm(ModelForm):
    
    class Meta:
        model=Cart
        fields=["producto","cantidad","observaciones"]
        
class CartPromocionesForm(ModelForm):
    lista_promociones= Promocion.objects.all()
    id_promocion=forms.ModelChoiceField(widget=forms.RadioSelect, queryset=lista_promociones)
    cantidad=forms.IntegerField(initial=1)
    class Meta:
        model=CartPromociones
        fields=["id_promocion","cantidad"]
    
        
#FORMULARIO EMPANADAS         
class CartEmpanadasForm(ModelForm):
    #LISTA DE PRODUCTOS, FILTRO POR CATEGORÍA
    lista_prod=Producto.objects.filter(categoria=1)
    #MOSTRAR LOS ELEMENTOS COMO UN CHOICEFIELD
    producto=forms.ModelChoiceField(widget=forms.RadioSelect, queryset=lista_prod)

    class Meta:
        model=Cart
        fields=["producto","cantidad","observaciones"]

#FORMULARIO PIZZAS
class CartPizzasForm(ModelForm):
    #LISTA DE PRODUCTOS, FILTRO POR CATEGORÍA
    lista_prod=Producto.objects.filter(categoria=2)
    #MOSTRAR LOS ELEMENTOS COMO UN CHOICEFIELD
    producto=forms.ModelChoiceField(widget=forms.RadioSelect, queryset=lista_prod)

    class Meta:
        model=Cart
        fields=["producto","cantidad","observaciones"]

#FORMULARIO CALZONES        
class CartCalzonesForm(ModelForm):
    #LISTA DE PRODUCTOS, FILTRO POR CATEGORÍA
    lista_prod=Producto.objects.filter(categoria=3)
    #MOSTRAR LOS ELEMENTOS COMO UN CHOICEFIELD
    producto=forms.ModelChoiceField(widget=forms.RadioSelect, queryset=lista_prod)

    class Meta:
        model=Cart
        fields=["producto","cantidad","observaciones"]
        
#FORMULARIO CANASTITAS        
class CartCanastitasForm(ModelForm):
    #LISTA DE PRODUCTOS, FILTRO POR CATEGORÍA
    lista_prod=Producto.objects.filter(categoria=4)
    #MOSTRAR LOS ELEMENTOS COMO UN CHOICEFIELD
    producto=forms.ModelChoiceField(widget=forms.RadioSelect, queryset=lista_prod)

    class Meta:
        model=Cart
        fields=["producto","cantidad","observaciones"]
        
#FORMULARIO CANASTITAS        
class CartOtrosForm(ModelForm):
    #LISTA DE PRODUCTOS, FILTRO POR CATEGORÍA
    lista_prod=Producto.objects.filter(categoria=5)
    #MOSTRAR LOS ELEMENTOS COMO UN CHOICEFIELD
    producto=forms.ModelChoiceField(widget=forms.RadioSelect, queryset=lista_prod)

    class Meta:
        model=Cart
        fields=["producto","cantidad","observaciones"]
        
