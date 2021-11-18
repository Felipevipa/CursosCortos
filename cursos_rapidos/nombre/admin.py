from django.contrib import admin
from .models import EstudianteProfile, Carrera, Calificacion, Tematica, Quiz, Material, Pregunta, OpcionRespuesta, Respuesta, Materia, Docente
# Register your models here.

admin.site.register(EstudianteProfile)
admin.site.register(Carrera)
admin.site.register(Calificacion)
# admin.site.register(Tematica)
admin.site.register(Quiz)
admin.site.register(Material)
admin.site.register(Pregunta)
admin.site.register(OpcionRespuesta)
admin.site.register(Respuesta)
admin.site.register(Materia)
admin.site.register(Docente)


# @admin.register(EstudianteProfile)
# class EstudianteAdmin(admin.ModelAdmin):
# 	# fields = (('name','venue'), 'event_date', 'description', 'manager')
# 	list_display = ('codigo', 'nombres', 'apellidos', 'documento', 'carrera')
# 	list_filter = ('carrera',)
# 	ordering = ('-nombres',)
		

@admin.register(Tematica)
class TematicaAdmin(admin.ModelAdmin):
	# fields = (('name','venue'), 'event_date', 'description', 'manager')
	list_display = ('titulo', 'materia', 'docente', 'last_updated',)
	list_filter = ('titulo', 'materia', 'docente', 'last_updated')
	ordering = ('-materia',)
