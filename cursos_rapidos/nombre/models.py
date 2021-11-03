from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import datetime
from django.urls import reverse

# Create your models here.
#'id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'))



class Carrera(models.Model):
    nombre      = models.CharField(max_length=50)

    def __str__(self):
        return '%s' % self.nombre

    def get_absolute_url(self):
        return reverse("ver-carrera", kwargs={'nombre': self.nombre})  # f"/products/{self.id}/"


class Estudiante(models.Model):
    foto        = models.ImageField(null=True, upload_to='static/images/estudiantes/')
    codigo      = models.BigIntegerField()
    nombres     = models.CharField(max_length=40)
    apellidos   = models.CharField(max_length=40)
    documento   = models.BigIntegerField()
    fechadenacimiento = models.DateField()
    email       = models.EmailField()
    usuario     = models.CharField(max_length=50)
    contrasena  = models.CharField(max_length=18)
    carrera     = models.ForeignKey(Carrera, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '%s %s' % (self.nombres, self.apellidos)


class Materia(models.Model):
    nombre = models.CharField(max_length=40)
    carrera = models.ForeignKey(Carrera, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '%s - %s' % (self.nombre, self.carrera)

    def get_absolute_url(self):
        return reverse("ver-materia", kwargs={'carrera': self.carrera, 'nombre': self.nombre})  # f"/products/{self.id}/"


class DocenteManager(BaseUserManager):

    def crear_docente(self, email, username, password=None):
        if not email:
            raise ValueError("Falta el correo electronico")
        if not username:
            raise ValueError("Falta el usuario")

        user = self.model(
            email = self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user





class Docente(AbstractBaseUser):
    foto              = models.ImageField(null=True)
    nombres           = models.CharField(max_length=40)
    apellidos         = models.CharField(max_length=40)
    documento         = models.BigIntegerField()
    fechadenacimiento = models.DateField()
    email             = models.EmailField(verbose_name="email", max_length=60, unique=True)
    usuario           = models.CharField(max_length=30, unique=30)
    carrera           = models.ForeignKey(Carrera, on_delete=models.SET_NULL, null=True)
    date_joined       = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login        = models.DateTimeField(verbose_name="last login", auto_now=True)
    hide_email        = models.BooleanField(default=True)
    is_admin          = models.BooleanField(default=False)

    objects = DocenteManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = '__all__'


    def __str__(self):
        return '%s %s' % (self.nombres, self.apellidos)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Tematica(models.Model):
    id          = models.BigAutoField(primary_key=True, serialize=False)
    titulo      = models.CharField(max_length=40)
    materia     = models.ForeignKey(Materia, on_delete=models.SET_NULL, null=True, blank=True)
    docente     = models.ForeignKey(Docente, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return '%s - %s' % (self.titulo, self.materia)

    def get_absolute_url(self):
        return reverse("ver-tematica", kwargs={'carrera': self.materia.carrera, 'materia': self.materia.nombre, 'titulo': self.titulo})


class Material(models.Model):
    contenido_de_texto = models.TextField(null=True, blank=True)
    imagen             = models.ImageField(null=True, blank=True, upload_to='static/images/material/')
    video              = models.URLField(null=True, blank=True)
    materialExterno    = models.URLField(null=True, blank=True)
    tematica           = models.ForeignKey(Tematica, on_delete=models.SET_NULL, null=True)


class Quiz(models.Model):
    tematica    = models.ForeignKey(Tematica, on_delete=models.SET_NULL, null=True)


class Calificacion(models.Model):
    fecha       = models.DateTimeField()
    tiempo      = models.TimeField()
    nota        = models.DecimalField(max_digits=2, decimal_places=2)
    quiz        = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True)
    estudiante  = models.ForeignKey(Estudiante, on_delete=models.SET_NULL, null=True)


class Pregunta(models.Model):
    enunciado   = models.TextField()
    quiz        = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True)


class OpcionRespuesta(models.Model):
    texto_corto   = models.CharField(max_length=100, null=True)
    texto_largo   = models.TextField()
    opcion_logica = models.BooleanField(default=False)
    pregunta      = models.ForeignKey(Pregunta, on_delete=models.SET_NULL, null=True)


class Respuesta(models.Model):
    respuesta_correcta = models.ForeignKey(OpcionRespuesta, on_delete=models.SET_NULL, null=True)
