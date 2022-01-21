from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.contrib.auth.models import User
import datetime
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
#'id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'))



class Carrera(models.Model):
    nombre      = models.CharField(max_length=50)

    def __str__(self):
        return '%s' % self.nombre

    def get_absolute_url(self):
        return reverse("ver-carrera", kwargs={'nombre': self.nombre})  # f"/products/{self.id}/"


class EstudianteProfile(models.Model):
    foto        = models.ImageField(null=True, upload_to='static/images/estudiantes/')
    codigo      = models.BigIntegerField()
    documento   = models.BigIntegerField()
    fechadenacimiento = models.DateField()
    user        = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    carrera     = models.ForeignKey(Carrera, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '%s %s' % (self.codigo, self.user.first_name)


class DocenteProfile(models.Model):
    foto              = models.ImageField(null=True, upload_to='static/images/docentes/')
    documento         = models.BigIntegerField()
    fechadenacimiento = models.DateField()
    carrera           = models.ForeignKey(Carrera, on_delete=models.SET_NULL, blank=True, null=True)
    user              = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)



class Materia(models.Model):
    nombre = models.CharField(max_length=40)
    carrera = models.ForeignKey(Carrera, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '%s - %s' % (self.nombre, self.carrera)

    def get_absolute_url(self):
        return reverse("ver-materia", kwargs={'carrera': self.carrera, 'nombre': self.nombre})  # f"/products/{self.id}/"




class Tematica(models.Model):
    id           = models.BigAutoField(primary_key=True, serialize=False)
    imagen       = models.ImageField(null=True, upload_to='static/images/tematicas/',)
    titulo       = models.CharField(max_length=80)
    resumen      = models.CharField(max_length=300,)
    materia      = models.ForeignKey(Materia, on_delete=models.SET_NULL, null=True, blank=True)
    docente      = models.ForeignKey(DocenteProfile, on_delete=models.SET_NULL, null=True, blank=True)
    is_available = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
    color1       = models.CharField(max_length=9)
    color2       = models.CharField(max_length=9)

    def __str__(self):
        return '%s - %s' % (self.titulo, self.materia)

    def get_absolute_url(self):
        return reverse("ver-tematica", kwargs={'carrera': self.materia.carrera, 'materia': self.materia.nombre, 'id': self.id})


class Enrolamiento(models.Model):
    estudianteProfile   = models.ForeignKey(EstudianteProfile, on_delete=models.SET_NULL, null=True)
    tematica            = models.ForeignKey(Tematica, on_delete=models.SET_NULL, null=True)


class Quiz(models.Model):
    titulo      = models.CharField(max_length=80, blank=True)
    tematica    = models.ForeignKey(Tematica, on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        return reverse("quiz", kwargs={'carrera': self.tematica.materia.carrera, 'materia': self.tematica.materia.nombre, 'tematica': self.tematica.id, 'id': self.id,})


class Material(models.Model):
    titulo             = models.CharField(max_length=80, blank=True)
    contenido_de_texto = models.TextField(null=True, blank=True)
    imagen             = models.ImageField(null=True, blank=True, upload_to='static/images/material/')
    video              = models.URLField(null=True, blank=True)
    materialExterno    = models.URLField(null=True, blank=True)
    tematica           = models.ForeignKey(Tematica, on_delete=models.SET_NULL, null=True)
    quizes             = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return 'tematica asociada: %s' % self.tematica


    def __str__(self):
        return '%s - %s' % (self.id, self.tematica)

    def get_absolute_url(self):
        return reverse("quiz", kwargs={'carrera': self.tematica.materia.carrera, 'materia': self.tematica.materia.nombre, 'tematica': self.tematica.titulo, 'id': self.id,})


class Calificacion(models.Model):
    fecha       = models.DateTimeField()
    tiempo      = models.TimeField()
    nota        = models.DecimalField(max_digits=4, decimal_places=2)
    quiz        = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True)
    estudiante  = models.ForeignKey(EstudianteProfile, on_delete=models.SET_NULL, null=True)


class Pregunta(models.Model):
    enunciado   = models.TextField()
    answer_type = models.CharField(max_length=10)
    quiz        = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True)


class OpcionRespuestaCerrada(models.Model):
    opcion_multiple     = models.CharField(max_length=100, null=True, blank=True)
    respuesta_correcta  = models.BooleanField(default=False, null=True, blank=True)
    pregunta            = models.ForeignKey(Pregunta, on_delete=models.CASCADE, null=True)


class OpcionRespuestaAbierta(models.Model):
    respuesta           = models.TextField(null=True, blank=True)
    pregunta            = models.ForeignKey(Pregunta, on_delete=models.SET_NULL, null=True)


class RespuestaEstudianteAbierta(models.Model):
    respuesta           = models.TextField(null=True, blank=True)
    pregunta            = models.ForeignKey(Pregunta, on_delete=models.SET_NULL, null=True)
    estudianteProfile   = models.ForeignKey(EstudianteProfile, on_delete=models.SET_NULL, null=True)
