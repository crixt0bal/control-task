from django.contrib import admin
from .models import Empleado, Tarea

# Register your models here.

admin.site.register(Empleado)
admin.site.register(Tarea)