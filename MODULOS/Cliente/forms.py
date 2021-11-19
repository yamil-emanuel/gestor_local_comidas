from django.db.models import fields
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.db.models.base import Model
from django import forms

from django.forms import ModelForm, ModelChoiceField
from .models import  SI_NO, Cliente


class ClienteForm(ModelForm):
    nombre = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Nombre del cliente', 'label':None, 'autocomplete': 'off'}))
    calle= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Calle', 'label':None, 'autocomplete': 'off'}))
    altura= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Altura', 'label':None, 'autocomplete': 'off'}))
    piso= forms.CharField(required=False, label='Piso', 
                    widget=forms.TextInput(attrs={'placeholder': 'Piso (opcional)'}))
    telefono= forms.IntegerField(label='Telefono*', 
                    widget=forms.TextInput(attrs={'placeholder': 'Telefono del cliente'}))
    
    es_whatsapp= forms.ChoiceField(label="¿Es WhatsApp?*", choices=SI_NO)
    
    telefono2= forms.IntegerField(label='Telefono 2', required=False,
                    widget=forms.TextInput(attrs={'placeholder': 'Telefono secundario (opcional)'}))
    
    class Meta:
        model=Cliente
        fields=["nombre","calle","altura","piso","telefono","es_whatsapp","telefono2"]



class CustomAuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'forms-html-container', 'placeholder': 'Username'})
        self.fields['username'].label = False
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'forms-html-container', 'placeholder':'Password'}) 
        self.fields['password'].label = False

    class Meta:
        model = User
        fields = ['username','password']



class NewUserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Inserte su usuario'
        self.fields['username'].widget.attrs['label'] = ''
        self.fields['password1'].widget.attrs['placeholder'] = 'Inserte una contraseña'
        self.fields['password1'].widget.attrs['label'] = ''    
        self.fields['email'].widget.attrs['placeholder'] = 'Inserte su email'
        self.fields['email'].widget.attrs['label'] = ''
        self.fields['password2'].widget.attrs['placeholder'] = 'Repita su contraseña'
        self.fields['password2'].widget.attrs['label'] = '' 
        
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        labels={"username":"","email":"","password1":"", "password2":""}


def save(self, commit=True):
    user = super(NewUserForm, self).save(commit=False)
    user.email = self.cleaned_data['email']
    if commit:
        user.save()
    return user