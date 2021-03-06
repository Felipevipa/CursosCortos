from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('',                                                                   views.home,                 name="home"),
    path('ver_perfil/<usuario>',                                               views.usuario,              name="user-detail"),
    path('categorias/',                                                        views.categorias_view,      name="ver-categorias"),
    path('categorias/<str:nombre>/',                                           views.ver_categoria,        name="ver-categoria"),
    path('categorias/<categoria>/agregar_tematica/',                           views.agregar_tematica,     name="agregar-tematica"),
    path('categorias/<categoria>/actualizar_tematica/<materia_id>',            views.actualizar_tematica,  name="actualizar-tematica"),
    path('categorias/<categoria>/eliminar_tematica/<materia_id>',              views.eliminar_tematica,    name="eliminar-tematica"),
    path('categorias/<categoria>/<str:nombre>/',                               views.ver_tematica,         name="ver-tematica"),
    path('categorias/<categoria>/<materia>/agregar_curso',                     views.agregar_curso,        name="agregar-curso"),
    path('categorias/<categoria>/<materia>/actualizar_curso/<tematica_id>',    views.actualizar_curso,     name="actualizar-curso"),
    path('categorias/<categoria>/<materia>/eliminar_curso/<tematica_id>',      views.eliminar_curso,       name="eliminar-curso"),
    path('categorias/<categoria>/<materia>/<tematica>/agregar_material',       views.agregar_material,     name="agregar-material"),
    path('categorias/<categoria>/<materia>/<tematica>/<id>actualizar_material',views.actualizar_material,  name="actualizar-material"),
    path('categorias/<categoria>/<materia>/<tematica>/<id>eliminar_material',  views.eliminar_material,    name="eliminar-material"),
    path('categorias/<categoria>/<materia>/<tematica>/agregar_quiz',           views.agregar_quiz,         name="agregar-quiz"),
    path('categorias/<categoria>/<materia>/<tematica>/<quiz>/agregar_pregunta',views.agregar_pregunta,     name="agregar-pregunta"),
    path('categorias/<categoria>/<materia>/<tematica>/<quiz>/<pregunta>/agregar_respuesta', views.agregar_respuesta,    name="agregar-respuesta"),
    path('categorias/<categoria>/<str:materia>/<id>/',                         views.ver_curso,            name="ver-curso"),
    path('categorias/<categoria>/<str:materia>/<tematica>/<id>',               views.quiz,                 name="quiz"),
    path('search_tematica/',                                                   views.search_tematica,      name="search-tematica"),
    path('agregar_carrera/',                                                   views.agregar_carrera,      name="agregar-carrera"),
    path('actualizar_carrera/<carrera_id>/',                                   views.actualizar_carrera,   name="actualizar-carrera"),
    path('eliminar_categoria/<categoria_id>/',                                 views.eliminar_categoria,   name="eliminar-carrera"),
    path('preguntar/',                                                         views.preguntar,            name="preguntar"),
    path('calificaciones/',                                                    views.calificaciones,       name="calificaciones"),
    path('calificaciones/chart',                                               views.calificaciones_chart, name="calificaciones_chart"),
    path('login_requerido',                                                    views.login_requerido,      name="login_requerido"),
       
]
