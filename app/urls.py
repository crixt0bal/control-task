from django.urls import path
from .views import home, crearusuario, listarusuario, listartarea, creartarea, crearunidadinterna, asignarrol, modificartarea, modificarusuario, finalizartarea, finalizarempleado, listadotareaprocesos



urlpatterns = [
    path('', home, name="home"),
    path('crearusuario/', crearusuario, name="crearusuario"),
    path('listarusuario/', listarusuario, name="listarusuario"),
    path('listartarea/', listartarea, name="listartarea"),
    path('tareas-procesos/', listadotareaprocesos, name="tareas-procesos"),
    path('creartarea/', creartarea, name="creartarea"),
    path('crearunidadinterna/', crearunidadinterna, name="crearunidadinterna"),
    path('asignarrol/', asignarrol, name="asignarrol"),
    path('modificartarea/<id>', modificartarea, name="modificartarea"),
    path('modificarusuario/<rut>', modificarusuario, name="modificarusuario"),
    path('finalizartarea/<id>', finalizartarea, name="finalizartarea"),
    path('finalizarempleado/<rut>', finalizarempleado, name="finalizarempleado"),
]