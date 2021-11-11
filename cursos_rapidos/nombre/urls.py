from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('',                                                           views.home,                 name="home"),
    path('registro/',                                                   views.registro,             name="registro"),
    path('<int:id>/',                                                   views.usuario,              name="user-detail"),
    path('carreras/',                                                   views.carreras_view,        name="carreras-detail"),
    path('carreras/<str:nombre>/',                                      views.ver_carrera,          name="ver-carrera"),
    path('carreras/<carrera>/agregar_materia/',                         views.agregar_materia,      name="agregar-materia"),
    path('carreras/<carrera>/actualizar_materia/<materia_id>',          views.actualizar_materia,   name="actualizar-materia"),
    path('carreras/<carrera>/eliminar_materia/<materia_id>',            views.eliminar_materia,     name="eliminar-materia"),
    path('carreras/<str:carrera>/<str:nombre>/',                        views.ver_materia,          name="ver-materia"),
    path('carreras/<carrera>/<materia>/agregar_tematica',               views.agregar_tematica,     name="agregar-tematica"),
    path('carreras/<carrera>/<materia>/actualizar_tematica/<tematica_id>',views.actualizar_tematica,name="actualizar-tematica"),
    path('carreras/<carrera>/<materia>/eliminar_tematica/<tematica_id>',views.eliminar_tematica,    name="eliminar-tematica"),
    path('carreras/<str:carrera>/<str:materia>/<str:titulo>/',          views.ver_tematica,         name="ver-tematica"),
    path('search_tematica/',                                            views.search_tematica,      name="search-tematica"),
    path('agregar_carrera/',                                            views.agregar_carrera,      name="agregar-carrera"),
    path('actualizar_carrera/<carrera_id>/',                            views.actualizar_carrera,   name="actualizar-carrera"),
    path('eliminar_carrera/<carrera_id>/',                              views.eliminar_carrera,     name="eliminar-carrera"),
    path('preguntar/',                                                  views.preguntar,            name="preguntar"),
]
