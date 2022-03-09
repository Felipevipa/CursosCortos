from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Categoria)
admin.site.register(Calificacion)
# admin.site.register(Tematica)
admin.site.register(Quiz)
admin.site.register(Material)
admin.site.register(Pregunta)
admin.site.register(OpcionRespuestaCerrada)
admin.site.register(OpcionRespuestaAbierta)
admin.site.register(Enrolamiento)
admin.site.register(Tematica)
admin.site.register(RespuestaUsuarioAbierta)
admin.site.register(Curso)
admin.site.register(PalabrasClaveRespuestaAbierta)


# @admin.register(EstudianteProfile)
# class EstudianteAdmin(admin.ModelAdmin):
# 	# fields = (('name','venue'), 'event_date', 'description', 'manager')
# 	list_display = ('codigo', 'nombres', 'apellidos', 'documento', 'carrera')
# 	list_filter = ('carrera',)
# 	ordering = ('-nombres',)
		

# @admin.register(Tematica)
# class TematicaAdmin(admin.ModelAdmin):
# 	# fields = (('name','venue'), 'event_date', 'description', 'manager')
# 	list_display = ('titulo', 'materia', 'docente', 'last_updated',)
# 	list_filter = ('titulo', 'materia', 'docente', 'last_updated')
# 	ordering = ('-materia',)
