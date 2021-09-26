from django.db.models import fields

from django.db.models.base import Model
from django import forms
from django.forms import ModelForm, ModelChoiceField
from .models import Reclamo
       
class ReclamosForm(ModelForm):
    class Meta:
        model=Reclamo
        fields=["observaciones","empleado"]