
from django.db.models import fields

from django.db.models.base import Model
from django import forms
from django.forms import ModelForm, ModelChoiceField
from .models import  MediosContacto, MediosPagos, MEDIO_CONTACTO, MEDIOS_PAGO, TiposEnvios

from MODULOS.Inventario.models import Promocion
from .models import Pedido

class PedidosForm(ModelForm):
    observaciones= forms.CharField(label='Observaciones', required=False,
                    widget=forms.TextInput(attrs={'placeholder': '(opcional)'}))
    class Meta:
        model=Pedido
        fields=["medio_pago","tipo_envio","medio_contacto","paga_con", "observaciones"]
        
class MotoForm(ModelForm):
    class Meta:
        model=Pedido
        fields=["moto"]

