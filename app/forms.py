from asyncio.windows_events import NULL
from email.policy import default
from logging import PlaceHolder
from msilib.schema import CheckBox
from random import choices
from secrets import choice
from select import select
from xmlrpc.client import DateTime
from django import forms
from .models import Empleado, Tarea, UnidadInterna
from django.forms import ValidationError

class DateTimeInput(forms.DateTimeInput):
   input_type = "datetime-local"

class CrearEmpleadoForm(forms.ModelForm):

    rut = forms.CharField(min_length=8, max_length=9, required=True, widget=forms.TextInput(attrs={'placeholder':'Ingrese rut', 'id':'rut_validation'}))
    nombres = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'Ingrese nombres'}))
    apellidos = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'Ingrese apellidos'}))
    correo_electronico = forms.EmailField(max_length=100, required=True, widget=forms.EmailInput(attrs={'placeholder':'Ingrese correo', 'id':'email_validation'}))
    usuario = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'Ingrese usuario'}))
    contrasena = forms.CharField(max_length=100, required=True, label="Contraseña", widget=forms.PasswordInput(attrs={'placeholder':'Ingrese contraseña', 'id':'contrasena_validation'}))

    #activo hidden
    activo = forms.IntegerField(widget=forms.HiddenInput, initial=1)

    


    class Meta:
        model = Empleado
        fields = '__all__'




class CrearTareaForm(forms.ModelForm):
    descripcion = forms.CharField(max_length=500, required=True, widget=forms.TextInput(attrs={'placeholder':'Ingrese Descripcion'}))
    inicio = forms.DateTimeField(
        input_formats= ['%Y-%m-%dT%H:%M'],
        required=True,
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }
        ))
    termino = forms.DateTimeField(
        input_formats= ['%Y-%m-%dT%H:%M'],
        required=True,
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }
        ))
    activo = forms.IntegerField(widget=forms.HiddenInput, initial=1)
    nombre = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder':'Ingrese nombre'}))

    repetible = forms.IntegerField(required=True)

    
    tarea_anterior = forms.Select()
    


    class Meta:
        model = Tarea
        fields = '__all__'


class AsignarRolForm(forms.ModelForm):
    rut = forms.CharField(min_length=8, max_length=9, required=True, widget=forms.TextInput(attrs={'placeholder':'Ingrese rut'}))

    class Meta:
        model = Empleado
        fields = ["rut", "cargo_empleado"]

#objetos_empresa = [
#    [1, 'SPA Ltda.']
#]

class UnidadInternaForm(forms.ModelForm):
    #id_empresa = forms.ChoiceField(widget=forms.Select, choices=objetos_empresa, label='Empresa', required=False)
    descripcion = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder':'Ingrese Descripcion'}))

    class Meta:
        model = UnidadInterna
        fields = '__all__'

class ModificarTareaForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput)
    descripcion = forms.CharField(max_length=500, required=True, widget=forms.TextInput(attrs={'placeholder':'Ingrese Descripcion'}))
    inicio = forms.DateTimeField(
        input_formats= ['%Y-%m-%dT%H:%M'],
        required=True,
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }
        ))
    termino = forms.DateTimeField(
        input_formats= ['%Y-%m-%dT%H:%M'],
        required=True,
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }
        ))
    activo = forms.IntegerField(widget=forms.HiddenInput, initial=1)
    nombre = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder':'Ingrese nombre'}))

    repetible = forms.IntegerField(required=True)
    


    class Meta:
        model = Tarea
        fields = '__all__'

class ModificarEmpleadoForm(forms.ModelForm):
    
    rut = forms.CharField(min_length=8, max_length=9, required=True, widget=forms.HiddenInput(attrs={'placeholder':'Ingrese rut', 'id':'rut_validation'}))
    nombres = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'Ingrese nombres'}))
    apellidos = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'Ingrese apellidos'}))
    correo_electronico = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'Ingrese correo', 'id':'email_validation'}))
    usuario = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'Ingrese usuario'}))
    contrasena = forms.CharField(max_length=100, required=True, label="Contraseña", widget=forms.PasswordInput(attrs={'placeholder':'Ingrese contraseña', 'id':'contrasena_validation'}))

    #activo hidden
    activo = forms.IntegerField(widget=forms.HiddenInput, initial=1)


    class Meta:
        model = Empleado
        fields = '__all__'
    

class FinalizarTareaForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput)


    class Meta:
        model = Tarea
        fields = ["id"]

class FinalizarEmpleadoForm(forms.ModelForm):
    rut = forms.CharField(min_length=8, max_length=9, required=True, widget=forms.HiddenInput(attrs={'placeholder':'Ingrese rut', 'id':'rut_validation'}))


    class Meta:
        model = Empleado
        fields = ["rut"]

    