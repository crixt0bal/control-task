from email.headerregistry import Group
from secrets import choice
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
 

# Create your models here.

class CargoEmpleado(models.Model):
    nombre_cargo = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nombre_cargo

    class Meta:
        managed = False
        db_table = 'Cargo_empleado'


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **other_fields):
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username = username,
            **other_fields
        )
        user.is_active = True

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        return self.create_user(username, password, **other_fields)



class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        db_column='NombreUsuario', max_length=50, unique=True
    )
    password = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    cargo_empleado = models.ForeignKey(CargoEmpleado, models.DO_NOTHING, db_column='cargo_empleado', null=True)
    date_joined = models.DateTimeField(
        auto_now_add=True, db_column='FechaCreacion'
    )
    last_login = models.DateTimeField(
        auto_now_add=True, db_column='LastLogin'
    )
    is_staff = models.BooleanField(default=False, db_column='is_staff')
    is_active = models.BooleanField(default=True, db_column='Estado')
    is_profesional = models.BooleanField(default=False, db_column='is_profesional')
    

    objects = CustomUserManager()



    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    









class Empleado(models.Model):
    rut = models.CharField(primary_key=True, max_length=9)
    nombres = models.CharField(max_length=100, blank=True, null=True)
    apellidos = models.CharField(max_length=100, blank=True, null=True)
    correo_electronico = models.CharField(max_length=100, blank=True, null=True)
    usuario = models.CharField(max_length=50, blank=True, null=True)
    contrasena = models.CharField(max_length=255, blank=True, null=True)
    activo = models.IntegerField()
    cargo_empleado = models.ForeignKey(CargoEmpleado, models.DO_NOTHING, db_column='cargo_empleado')
    id_empresa = models.ForeignKey('Empresa', models.DO_NOTHING, db_column='id_empresa', blank=False, null=True)
    id_unida = models.ForeignKey('UnidadInterna', models.DO_NOTHING, db_column='id_unida', blank=False)

    def __str__(self):
        return self.rut
    

    class Meta:
        managed = False
        db_table = 'Empleado'


class Empresa(models.Model):
    nombre_empresa = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre_empresa

    class Meta:
        managed = False
        db_table = 'Empresa'

class UnidadInterna(models.Model):
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    id_empresa = models.ForeignKey(Empresa, models.DO_NOTHING, db_column='id_empresa')

    def __str__(self):
        return self.descripcion

    class Meta:
        managed = False
        db_table = 'Unidad_interna'

        

class EstadoTarea(models.Model):
    descripcion_estado = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.descripcion_estado

    class Meta:
        managed = False
        db_table = 'Estado_tarea'











class Tarea(models.Model):
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    inicio = models.DateTimeField(blank=True, null=True)
    termino = models.DateTimeField(blank=True, null=True)
    repetible = models.BooleanField(blank=False, null=True)
    activo = models.IntegerField()
    estado = models.ForeignKey(EstadoTarea, models.DO_NOTHING, db_column='estado', blank=False, null=True)
    creador = models.ForeignKey(Empleado, models.DO_NOTHING, db_column='creador')
    tarea_anterior = models.ForeignKey('self', models.DO_NOTHING, db_column='tarea_anterior', blank=False, null=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.descripcion

    

    class Meta:
        managed = False
        db_table = 'Tarea'
