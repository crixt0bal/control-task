from sqlite3 import Cursor, connect
from django.shortcuts import render, redirect, get_object_or_404
from app.models import Empleado, CargoEmpleado, Empresa, UnidadInterna, Tarea, EstadoTarea
from django.contrib import messages
from .forms import CrearEmpleadoForm, CrearTareaForm, AsignarRolForm, UnidadInternaForm, ModificarTareaForm, ModificarEmpleadoForm, FinalizarTareaForm, FinalizarEmpleadoForm
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required
def home(request):
    return render(request, 'app/home.html')




from django.db import connection

@login_required
def crearusuario(request):
    data = {
        'empleado': CrearEmpleadoForm()
    }
    if request.method=="POST":
        if request.POST.get('rut') and request.POST.get('nombres') and request.POST.get('apellidos') and request.POST.get('correo_electronico') and request.POST.get('usuario') and request.POST.get('contrasena') and request.POST.get('activo') and request.POST.get('cargo_empleado') and request.POST.get('id_empresa') and request.POST.get('id_unida'):
            usersave= Empleado()
            usersave.rut=request.POST.get('rut')
            usersave.nombres=request.POST.get('nombres')
            usersave.apellidos=request.POST.get('apellidos')
            usersave.correo_electronico=request.POST.get('correo_electronico')
            usersave.usuario=request.POST.get('usuario')
            usersave.contrasena=request.POST.get('contrasena')
            usersave.activo=request.POST.get('activo')
            usersave.cargo_empleado=CargoEmpleado.objects.get(pk=(request.POST.get('cargo_empleado')))
            usersave.id_empresa=Empresa.objects.get(pk=(request.POST.get('id_empresa')))
            usersave.id_unida=UnidadInterna.objects.get(pk=(request.POST.get('id_unida')))
            cursor=connection.cursor()
            cursor.execute("call SP_crear_usuario('"+usersave.rut+"','"+usersave.nombres+"', '"+usersave.apellidos+"', '"+usersave.correo_electronico+"', '"+usersave.usuario+"', '"+usersave.contrasena+"', '"+usersave.activo+"', '"+str(usersave.cargo_empleado.id)+"', '"+str(usersave.id_empresa.id)+"', '"+str(usersave.id_unida.id)+"')")
            messages.success(request, "El empleado "+usersave.nombres+" se guardo correctamente ")
            return render(request, 'app/crearusuario.html', data)
    else:
        return render(request, 'app/crearusuario.html', data)

@login_required
def creartarea(request):
    data = {
        'tarea': CrearTareaForm()
    }
    if request.method=="POST":
        if request.POST.get('nombre') and request.POST.get('descripcion') and request.POST.get('inicio') and request.POST.get('termino') and request.POST.get('repetible') and request.POST.get('activo') and request.POST.get('estado') and request.POST.get('creador') and request.POST.get('tarea_anterior'):
            tareasave= Tarea()
            tareasave.nombre=request.POST.get('nombre')
            tareasave.descripcion=request.POST.get('descripcion')
            tareasave.inicio=request.POST.get('inicio')
            tareasave.termino=request.POST.get('termino')
            tareasave.repetible=request.POST.get('repetible')
            tareasave.activo=request.POST.get('activo')
            tareasave.estado=EstadoTarea.objects.get(pk=(request.POST.get('estado')))
            tareasave.creador=Empleado.objects.get(rut=(request.POST.get('creador')))
            tareasave.tarea_anterior=Tarea(pk=(request.POST.get('tarea_anterior')))
            cursor=connection.cursor()
            cursor.execute("call SP_crear_tarea('"+tareasave.nombre+"','"+tareasave.descripcion+"', '"+tareasave.inicio+"', '"+tareasave.termino+"', '"+tareasave.repetible+"', '"+tareasave.activo+"', '"+str(tareasave.estado.id)+"', '"+str(tareasave.creador.rut)+"', '"+str(tareasave.tarea_anterior.id)+"')")
            messages.success(request, "La tarea "+tareasave.nombre+" se guardo correctamente ")
            return render(request, 'app/creartarea.html', data)
    else:
        return render(request, 'app/creartarea.html', data)

@login_required
def crearunidadinterna(request):
    data = {
        'unidadinterna': UnidadInternaForm()
    }
    if request.method=="POST":
        if request.POST.get('descripcion') and request.POST.get('id_empresa'):
            unidadsave= UnidadInterna()
            unidadsave.descripcion=request.POST.get('descripcion')
            unidadsave.id_empresa= Empresa.objects.get(pk=(request.POST.get('id_empresa')))
            cursor=connection.cursor()
            cursor.execute("call SP_crear_unidad_interna('"+unidadsave.descripcion+"','"+str(unidadsave.id_empresa.id)+"')")
            messages.success(request, "La unidad "+unidadsave.descripcion+" se guardo correctamente ")
            return render(request, 'app/crearunidad.html', data)
    else:
        return render(request, 'app/crearunidad.html', data)

@login_required
def listarusuario(request):
    cursor=connection.cursor()
    cursor.execute('call SP_listar_todos_empleados()')
    results=cursor.fetchall()
    
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(results, 6)
        results = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': results,
        'paginator': paginator
    }

    return render(request, 'app/listarusuario.html', data)

    
@login_required
def listartarea(request):

    cursor=connection.cursor()
    cursor.execute('call SP_listar_todas_tareas()')
    results=cursor.fetchall()

    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(results, 6)
        results = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': results,
        'paginator': paginator
    }

    return render(request, 'app/listartarea.html', data)


@login_required
def asignarrol(request):
    data = {
        'asignarrol': AsignarRolForm()
    }
    if request.method=="POST":
        if request.POST.get('rut') and request.POST.get('cargo_empleado'):
            rolupdate= Empleado()
            rolupdate.rut=request.POST.get('rut')
            rolupdate.cargo_empleado=CargoEmpleado.objects.get(pk=(request.POST.get('cargo_empleado')))
            cursor=connection.cursor()
            cursor.execute("call SP_asignar_rol('"+rolupdate.rut+"','"+str(rolupdate.cargo_empleado.id)+"')")
            messages.success(request, "Al empleado "+rolupdate.rut+" se le asigno un rol ")
            return render(request, 'app/asignarrol.html', data)
    else:
        return render(request, 'app/asignarrol.html', data)

@login_required
def modificartarea(request, id):

    tarea = get_object_or_404(Tarea, id=id)

    data = {
        'tarea': ModificarTareaForm(instance=tarea)
    }

    if request.method=="POST":
        if request.POST.get('id') and request.POST.get('nombre') and request.POST.get('descripcion') and request.POST.get('inicio') and request.POST.get('termino') and request.POST.get('repetible') and request.POST.get('activo') and request.POST.get('estado') and request.POST.get('creador') and request.POST.get('tarea_anterior'):
            tareaupdate= Tarea()
            tareaupdate.id=request.POST.get('id')
            tareaupdate.nombre=request.POST.get('nombre')
            tareaupdate.descripcion=request.POST.get('descripcion')
            tareaupdate.inicio=request.POST.get('inicio')
            tareaupdate.termino=request.POST.get('termino')
            tareaupdate.repetible=request.POST.get('repetible')
            tareaupdate.activo=request.POST.get('activo')
            tareaupdate.estado=EstadoTarea.objects.get(pk=(request.POST.get('estado')))
            tareaupdate.creador=Empleado.objects.get(rut=(request.POST.get('creador')))
            tareaupdate.tarea_anterior=Tarea(pk=(request.POST.get('tarea_anterior')))
            cursor=connection.cursor()
            cursor.execute("call SP_modificar_tarea('"+str(tareaupdate.id)+"','"+tareaupdate.nombre+"','"+tareaupdate.descripcion+"', '"+tareaupdate.inicio+"', '"+tareaupdate.termino+"', '"+tareaupdate.repetible+"', '"+tareaupdate.activo+"', '"+str(tareaupdate.estado.id)+"', '"+str(tareaupdate.creador.rut)+"', '"+str(tareaupdate.tarea_anterior.id)+"')")
            messages.success(request, "La tarea "+tareaupdate.nombre+" se edito correctamente ")

            return render(request, 'app/modificartarea.html', data)
    else:
        return render(request, 'app/modificartarea.html', data)


@login_required
def modificarusuario(request, rut):
    usuario = get_object_or_404(Empleado, rut=rut)

    data = {
        'empleado': ModificarEmpleadoForm(instance=usuario)
    }
    
    if request.method=="POST":
        if request.POST.get('rut') and request.POST.get('nombres') and request.POST.get('apellidos') and request.POST.get('correo_electronico') and request.POST.get('usuario') and request.POST.get('contrasena') and request.POST.get('activo') and request.POST.get('cargo_empleado') and request.POST.get('id_empresa') and request.POST.get('id_unida'):
            userupdate= Empleado()
            userupdate.rut=request.POST.get('rut')
            userupdate.nombres=request.POST.get('nombres')
            userupdate.apellidos=request.POST.get('apellidos')
            userupdate.correo_electronico=request.POST.get('correo_electronico')
            userupdate.usuario=request.POST.get('usuario')
            userupdate.contrasena=request.POST.get('contrasena')
            userupdate.activo=request.POST.get('activo')
            userupdate.cargo_empleado=CargoEmpleado.objects.get(pk=(request.POST.get('cargo_empleado')))
            userupdate.id_empresa=Empresa.objects.get(pk=(request.POST.get('id_empresa')))
            userupdate.id_unida=UnidadInterna.objects.get(pk=(request.POST.get('id_unida')))
            cursor=connection.cursor()
            cursor.execute("call SP_modificar_usuario('"+userupdate.rut+"','"+userupdate.nombres+"', '"+userupdate.apellidos+"', '"+userupdate.correo_electronico+"', '"+userupdate.usuario+"', '"+userupdate.contrasena+"', '"+userupdate.activo+"', '"+str(userupdate.cargo_empleado.id)+"', '"+str(userupdate.id_empresa.id)+"', '"+str(userupdate.id_unida.id)+"')")
            messages.success(request, "El empleado "+userupdate.nombres+" se guardo correctamente ")
            return render(request, 'app/modificarusuario.html', data)
    else:
        return render(request, 'app/modificarusuario.html', data)

@login_required
def finalizartarea(request, id):
    tarea = get_object_or_404(Tarea, id=id)

    data = {
        'tarea': FinalizarTareaForm(instance=tarea)
    }

    if request.method=="POST":
        if request.POST.get('id'):
            tareafinalizar= Tarea()
            tareafinalizar.id=request.POST.get('id')
            cursor=connection.cursor()
            cursor.execute("call SP_finalizar_tarea_2('"+str(tareafinalizar.id)+"')")
            messages.success(request, "La tarea finalizo correctamente ")
            return render(request, 'app/finalizartarea.html', data)
    else:
        return render(request, 'app/finalizartarea.html', data)


@login_required
def finalizarempleado(request, rut):
    empleado = get_object_or_404(Empleado, rut=rut)

    data = {
        'empleado': FinalizarEmpleadoForm(instance=empleado)
    }

    if request.method=="POST":
        if request.POST.get('rut'):
            empleadofinalizar= Tarea()
            empleadofinalizar.rut=request.POST.get('rut')
            cursor=connection.cursor()
            cursor.execute("call SP_finalizar_empleado('"+empleadofinalizar.rut+"')")
            messages.success(request, "El empleado se dio de baja correctamente ")
            return render(request, 'app/finalizarempleado.html', data)
    else:
        return render(request, 'app/finalizarempleado.html', data)






        