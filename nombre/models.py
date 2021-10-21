from django.db import models

# Create your models here.
#'id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'))


class Estudiante(models.Model):
    id          = models.BigAutoField(blank=True, null=False)
    usuario     = models.CharField(max_length=50)
    contrasena  = models.CharField(max_length=18)
    carrera     = models.BigAutoField(blank=True, null=False)

