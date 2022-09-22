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
import datetime
from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone
import re

class DateTimeInput(forms.DateTimeInput):
   input_type = "datetime-local"

class CrearEmpleadoForm(forms.ModelForm):

    rut = forms.CharField(min_length=8, max_length=9, required=True,
    validators=[RegexValidator('^[0-9]*$')], error_messages={'invalid': 'El rut debe contener solo numeros'}, widget=forms.TextInput(attrs={'placeholder':'Ingrese rut', 'id':'rut_validation'}))
    nombres = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'Ingrese nombres'}))
    apellidos = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'Ingrese apellidos'}))
    correo_electronico = forms.EmailField(max_length=100, required=True, widget=forms.EmailInput(attrs={'placeholder':'Ingrese correo', 'id':'email_validation'}))
    usuario = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'Ingrese usuario'}))
    contrasena = forms.CharField(max_length=100, required=True, label="Contraseña", validators=[RegexValidator('^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')], error_messages={'invalid': 'Debe contener mínimo ocho caracteres, al menos una letra y un número'}, widget=forms.PasswordInput(attrs={'placeholder':'Ingrese contraseña', 'id':'contrasena_validation'}))

    #activo hidden
    activo = forms.IntegerField(widget=forms.HiddenInput, initial=1)

    
    def clean_rut(self):
        rut = self.cleaned_data["rut"]
        existe = Empleado.objects.filter(rut__iexact=rut).exists()

        if existe:
            raise ValidationError("Este rut ya existe")
        return existe

    def clean_usuario(self):
        usuario = self.cleaned_data["usuario"]
        existe = Empleado.objects.filter(usuario__iexact=usuario).exists()

        if existe:
            raise ValidationError("Este usuario ya existe")
        return existe

    def clean_correo_electronico(self):
        correo_electronico = self.cleaned_data["correo_electronico"]
        existe = Empleado.objects.filter(correo_electronico__iexact=correo_electronico).exists()

        if existe:
            raise ValidationError("Este correo electronico ya existe")
        return existe


    class Meta:
        model = Empleado
        fields = '__all__'




class CrearTareaForm(forms.ModelForm):
    descripcion = forms.CharField(max_length=500, required=True, widget=forms.TextInput(attrs={'placeholder':'Ingrese Descripcion'}))
    inicio = forms.DateTimeField(
        input_formats= ['%Y-%m-%dT%H:%M'],
        required=True,
        validators=[MinValueValidator(timezone.now)],
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }
        ))

    def clean_inicio(self):
        inicio = self.cleaned_data['inicio']
        if inicio < timezone.now():
            raise forms.ValidationError("La fecha no puede ser menor a la de hoy!")
        return inicio

    termino = forms.DateTimeField(
        input_formats= ['%Y-%m-%dT%H:%M'],
        required=True,
        validators=[MinValueValidator(timezone.now)],
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }
        ))

    def clean_termino(self):
        termino = self.cleaned_data['termino']
        inicio = self.cleaned_data['inicio']
        if termino < timezone.now() or termino < inicio:
            raise forms.ValidationError("La fecha de termino no puede ser menor a la de hoy y no puede ser menor a la fecha de inicio!")
        return termino

    
    
    activo = forms.IntegerField(widget=forms.HiddenInput, initial=1)
    nombre = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder':'Ingrese nombre'}))

    repetible = forms.IntegerField(required=True)


    tarea_anterior = forms.Select()
    
    def clean_descripcion(self):
        descripcion = self.cleaned_data["descripcion"]
        existe = Tarea.objects.filter(descripcion__iexact=descripcion).exists()

        if existe:
            raise ValidationError("Esta descripcion ya existe")
        return existe
    
    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"]
        existe = Tarea.objects.filter(nombre__iexact=nombre).exists()

        if existe:
            raise ValidationError("Este nombre ya existe")
        return existe

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
        validators=[MinValueValidator(timezone.now)],
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }
        ))

    def clean_inicio(self):
        inicio = self.cleaned_data['inicio']
        if inicio < timezone.now():
            raise forms.ValidationError("La fecha no puede ser menor a la de hoy!")
        return inicio
    termino = forms.DateTimeField(
        input_formats= ['%Y-%m-%dT%H:%M'],
        required=True,
        validators=[MinValueValidator(timezone.now)],
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }
        ))

    def clean_termino(self):
        termino = self.cleaned_data['termino']
        if termino < timezone.now():
            raise forms.ValidationError("La fecha no puede ser menor a la de hoy!")
        return termino
    activo = forms.IntegerField(widget=forms.HiddenInput, initial=1)
    nombre = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder':'Ingrese nombre'}))

    repetible = forms.IntegerField(required=True)
    
    """
    def clean_descripcion(self):
        descripcion = self.cleaned_data["descripcion"]
        existe = Tarea.objects.filter(descripcion__iexact=descripcion).exists()

        if existe:
            raise ValidationError("Esta descripcion ya existe")
        return existe
    
    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"]
        existe = Tarea.objects.filter(nombre__iexact=nombre).exists()

        if existe:
            raise ValidationError("Este nombre ya existe")
        return existe
    """

    class Meta:
        model = Tarea
        fields = '__all__'

class ModificarEmpleadoForm(forms.ModelForm):
    
    rut = forms.CharField(min_length=8, max_length=9, required=True, widget=forms.HiddenInput(attrs={'placeholder':'Ingrese rut', 'id':'rut_validation'}))
    nombres = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'Ingrese nombres'}))
    apellidos = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'Ingrese apellidos'}))
    correo_electronico = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'Ingrese correo', 'id':'email_validation'}))
    usuario = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'Ingrese usuario'}))
    contrasena = forms.CharField(max_length=100, required=True, label="Contraseña", validators=[RegexValidator('^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')], error_messages={'invalid': 'Debe contener mínimo ocho caracteres, al menos una letra y un número'}, widget=forms.PasswordInput(attrs={'placeholder':'Ingrese contraseña', 'id':'contrasena_validation'}))

    #activo hidden
    activo = forms.IntegerField(widget=forms.HiddenInput, initial=1)


    """
    def clean_usuario(self):
        usuario = self.cleaned_data["usuario"]
        existe = Empleado.objects.filter(usuario__iexact=usuario).exists()

        if existe:
            raise ValidationError("Este usuario ya existe")
        return existe

    def clean_correo_electronico(self):
        correo_electronico = self.cleaned_data["correo_electronico"]
        existe = Empleado.objects.filter(correo_electronico__iexact=correo_electronico).exists()
    """

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

    