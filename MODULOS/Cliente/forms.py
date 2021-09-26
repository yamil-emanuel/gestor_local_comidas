from django.db.models import fields

from django.db.models.base import Model
from django import forms
from django.forms import ModelForm, ModelChoiceField
from .models import  SI_NO, Cliente


class ClienteForm(ModelForm):
    nombre = forms.CharField(label='Nombre*', 
                    widget=forms.TextInput(attrs={'placeholder': 'Nombre del cliente'}))
    calle= forms.CharField(label='Calle*', 
                    widget=forms.TextInput(attrs={'placeholder': 'Calle del cliente'}))
    altura= forms.CharField(label='Altura*', 
                    widget=forms.TextInput(attrs={'placeholder': 'Altura del cliente'}))
    piso= forms.CharField(required=False, label='Piso', 
                    widget=forms.TextInput(attrs={'placeholder': '(opcional)'}))
    telefono= forms.IntegerField(label='Telefono*', 
                    widget=forms.TextInput(attrs={'placeholder': 'Telefono del cliente'}))
    
    es_whatsapp= forms.ChoiceField(label="¿Es WhatsApp?*", choices=SI_NO)
    
    telefono2= forms.IntegerField(label='Telefono 2', required=False,
                    widget=forms.TextInput(attrs={'placeholder': '(opcional)'}))
    
    class Meta:
        model=Cliente
        fields=["nombre","calle","altura","piso","telefono","es_whatsapp","telefono2"]

