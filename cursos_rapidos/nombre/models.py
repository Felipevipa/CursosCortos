from django.db import models
import datetime

# Create your models here.
#'id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'))



class Carrera(models.Model):
    nombre      = models.CharField(max_length=50)

    def __str__(self):
        return '%s' % self.nombre


class Estudiante(models.Model):
    nombres     = models.CharField(max_length=40)
    apellidos   = models.CharField(max_length=40)
    documento   = models.IntegerField()
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
        return '%s %s' % (self.nombre, self.carrera)


class Docente(models.Model):
    nombres = models.CharField(max_length=40)
    apellidos = models.CharField(max_length=40)
    documento = models.IntegerField()
    fechadenacimiento = models.DateField()
    email = models.EmailField()
    usuario = models.CharField(max_length=50)
    contrasena = models.CharField(max_length=18)
    carrera = models.ForeignKey(Carrera, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '%s %s' % (self.nombres, self.apellidos)


class Tematica(models.Model):
    id          = models.BigAutoField(primary_key=True, serialize=False)
    titulo      = models.CharField(max_length=40)
    materia     = models.ForeignKey(Materia, on_delete=models.SET_NULL, null=True)
    docente     = models.ForeignKey(Docente, on_delete=models.SET_NULL, null=True)


class Material(models.Model):
    contenido_de_texto = models.TextField(null=True)
    imagen             = models.ImageField(null=True)
    video              = models.URLField(null=True)
    materialExterno    = models.URLField(null=True)
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