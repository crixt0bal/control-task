from django.contrib import admin
from .models import Empleado, Tarea, User

# Register your models here.

admin.site.register(Empleado)
admin.site.register(Tarea)
admin.site.register(User)