from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('',                                                                views.home,                 name="home"),
    path('ver_perfil/',                                                     views.usuario,              name="user-detail"),
    path('categorias/',                                                     views.categorias_view,      name="carreras-detail"),
    path('carreras/<str:nombre>/',                                          views.ver_carrera,          name="ver-carrera"),
    path('carreras/<carrera>/agregar_materia/',                             views.agregar_materia,      name="agregar-materia"),
    path('carreras/<carrera>/actualizar_materia/<materia_id>',              views.actualizar_materia,   name="actualizar-materia"),
    path('carreras/<carrera>/eliminar_materia/<materia_id>',                views.eliminar_materia,     name="eliminar-materia"),
    path('carreras/<str:carrera>/<str:nombre>/',                            views.ver_materia,          name="ver-materia"),
    path('carreras/<carrera>/<materia>/agregar_tematica',                   views.agregar_tematica,     name="agregar-tematica"),
    path('carreras/<carrera>/<materia>/actualizar_tematica/<tematica_id>',  views.actualizar_tematica,  name="actualizar-tematica"),
    path('carreras/<carrera>/<materia>/eliminar_tematica/<tematica_id>',    views.eliminar_tematica,    name="eliminar-tematica"),
    path('carreras/<carrera>/<materia>/<tematica>/agregar_material',        views.agregar_material,     name="agregar-material"),
    path('carreras/<carrera>/<materia>/<tematica>/<id>actualizar_material', views.actualizar_material,  name="actualizar-material"),
    path('carreras/<carrera>/<materia>/<tematica>/<id>eliminar_material',   views.eliminar_material,    name="eliminar-material"),
    path('carreras/<carrera>/<materia>/<tematica>/agregar_quiz',            views.agregar_quiz,         name="agregar-quiz"),
    path('carreras/<carrera>/<materia>/<tematica>/<quiz>/agregar_pregunta', views.agregar_pregunta,     name="agregar-pregunta"),
    path('carreras/<carrera>/<materia>/<tematica>/<quiz>/<pregunta>/agregar_respuesta', views.agregar_respuesta,    name="agregar-respuesta"),
    path('carreras/<str:carrera>/<str:materia>/<id>/',                      views.ver_tematica,         name="ver-tematica"),
    path('carreras/<str:carrera>/<str:materia>/<tematica>/<id>',            views.quiz,                 name="quiz"),
    path('search_tematica/',                                                views.search_tematica,      name="search-tematica"),
    path('agregar_carrera/',                                                views.agregar_carrera,      name="agregar-carrera"),
    path('actualizar_carrera/<carrera_id>/',                                views.actualizar_carrera,   name="actualizar-carrera"),
    path('eliminar_categoria/<categoria_id>/',                              views.eliminar_categoria,   name="eliminar-carrera"),
    path('preguntar/',                                                      views.preguntar,            name="preguntar"),
    path('calificaciones/',                                                 views.calificaciones,       name="calificaciones"),
    path('calificaciones/chart',                                            views.calificaciones_chart, name="calificaciones_chart"),
    path('login_requerido',                                                 views.login_requerido,      name="login_requerido"),
       
]
