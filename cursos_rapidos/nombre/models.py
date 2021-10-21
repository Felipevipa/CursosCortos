from django.db import models

# Create your models here.
#'id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'))


class Carrera(models.Model):
    nombre      = models.CharField(max_length=50)


class Estudiante(models.Model):
    usuario     = models.CharField(max_length=50)
    contrasena  = models.CharField(max_length=18)
    carrera     = models.ForeignKey(Carrera, on_delete=models.SET_NULL, null=True)


