from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.contrib.auth.models import User
import datetime
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
#'id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'))



class Categoria(models.Model):
    imagen      = models.ImageField(null=True, upload_to='static/images/categorias/')
    nombre      = models.CharField(max_length=50)

    def __str__(self):
        return '%s' % self.nombre

    def get_absolute_url(self):
        return reverse("ver-categoria", kwargs={'nombre': self.nombre})  # f"/products/{self.id}/"


class UserProfile(models.Model):
    foto        = models.ImageField(null=True, upload_to='static/images/estudiantes/')
    documento   = models.BigIntegerField()
    fechadenacimiento = models.DateField()
    user        = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)


class Tematica(models.Model):
    nombre = models.CharField(max_length=40)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '%s - %s' % (self.nombre, self.categoria)

    def get_absolute_url(self):
        return reverse("ver-tematica", kwargs={'categoria': self.categoria, 'nombre': self.nombre})  # f"/products/{self.id}/"




class Curso(models.Model):
    id           = models.BigAutoField(primary_key=True, serialize=False)
    imagen       = models.ImageField(null=True, upload_to='static/images/tematicas/',)
    titulo       = models.CharField(max_length=80)
    resumen      = models.CharField(max_length=300,)
    tematica     = models.ForeignKey(Tematica, on_delete=models.SET_NULL, null=True, blank=True)
    is_available = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
    color1       = models.CharField(max_length=9)
    color2       = models.CharField(max_length=9)

    def __str__(self):
        return '%s - %s' % (self.titulo, self.tematica)

    def get_absolute_url(self):
        return reverse("ver-curso", kwargs={'categoria': self.tematica.categoria.nombre, 'materia': self.tematica.nombre, 'id': self.id})


class Enrolamiento(models.Model):
    userProfile   = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    curso         = models.ForeignKey(Curso, on_delete=models.CASCADE, null=True)
    isCreator     = models.BooleanField(default=False)
    isEnroled     = models.BooleanField(default=False)


class Quiz(models.Model):
    titulo      = models.CharField(max_length=80, blank=True)
    curso       = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        return reverse("quiz", kwargs={'categoria': self.curso.tematica.categoria, 'materia': self.curso.tematica.nombre, 'tematica': self.curso.id, 'id': self.id,})


class Material(models.Model):
    titulo             = models.CharField(max_length=80, blank=True)
    contenido_de_texto = models.TextField(null=True, blank=True)
    imagen             = models.ImageField(null=True, blank=True, upload_to='static/images/material/')
    video              = models.URLField(null=True, blank=True)
    materialExterno    = models.URLField(null=True, blank=True)
    curso              = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True, blank=True)
    quizes             = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return 'tematica asociada: %s' % self.curso


    def __str__(self):
        return '%s - %s' % (self.id, self.curso)

    def get_absolute_url(self):
        return reverse("quiz", kwargs={'carrera': self.tematica.materia.carrera, 'materia': self.tematica.materia.nombre, 'tematica': self.tematica.titulo, 'id': self.id,})


class Calificacion(models.Model):
    fecha       = models.DateTimeField()
    tiempo      = models.TimeField()
    nota        = models.DecimalField(max_digits=4, decimal_places=2)
    quiz        = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True)
    userProfile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)


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
    pregunta            = models.ForeignKey(Pregunta, on_delete=models.CASCADE, null=True)
    valoracion          = models.IntegerField()


class PalabrasClaveRespuestaAbierta(models.Model):

    palabra  = models.CharField(max_length=50)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, null=True)
    
    class Meta:
        verbose_name = "PalabrasClaveRespuestaAbierta"
        verbose_name_plural = "PalabrasClaveRespuestaAbiertas"

    def __str__(self):
        return self.palabra



class RespuestaUsuarioAbierta(models.Model):
    respuesta   = models.TextField(null=True, blank=True)
    pregunta    = models.ForeignKey(Pregunta, on_delete=models.SET_NULL, null=True)
    userProfile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
