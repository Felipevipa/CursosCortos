# Generated by Django 3.2.8 on 2021-11-04 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carrera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('foto', models.ImageField(null=True, upload_to='')),
                ('nombres', models.CharField(max_length=40)),
                ('apellidos', models.CharField(max_length=40)),
                ('documento', models.BigIntegerField()),
                ('fechadenacimiento', models.DateField()),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('usuario', models.CharField(max_length=30, unique=30)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('hide_email', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('carrera', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='nombre.carrera')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40)),
                ('carrera', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='nombre.carrera')),
            ],
        ),
        migrations.CreateModel(
            name='OpcionRespuesta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto_corto', models.CharField(max_length=100, null=True)),
                ('texto_largo', models.TextField()),
                ('opcion_logica', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Tematica',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('imagen', models.ImageField(null=True, upload_to='static/images/tematicas/')),
                ('titulo', models.CharField(max_length=40)),
                ('resumen', models.CharField(max_length=200)),
                ('is_available', models.BooleanField(default=False)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('docente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='nombre.docente')),
                ('materia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='nombre.materia')),
            ],
        ),
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('respuesta_correcta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='nombre.opcionrespuesta')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tematica', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='nombre.tematica')),
            ],
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enunciado', models.TextField()),
                ('quiz', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='nombre.quiz')),
            ],
        ),
        migrations.AddField(
            model_name='opcionrespuesta',
            name='pregunta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='nombre.pregunta'),
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenido_de_texto', models.TextField(blank=True, null=True)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='static/images/material/')),
                ('video', models.URLField(blank=True, null=True)),
                ('materialExterno', models.URLField(blank=True, null=True)),
                ('tematica', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='nombre.tematica')),
            ],
        ),
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.ImageField(null=True, upload_to='static/images/estudiantes/')),
                ('codigo', models.BigIntegerField()),
                ('nombres', models.CharField(max_length=40)),
                ('apellidos', models.CharField(max_length=40)),
                ('documento', models.BigIntegerField()),
                ('fechadenacimiento', models.DateField()),
                ('email', models.EmailField(max_length=254)),
                ('usuario', models.CharField(max_length=50)),
                ('contrasena', models.CharField(max_length=18)),
                ('carrera', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='nombre.carrera')),
            ],
        ),
        migrations.CreateModel(
            name='Calificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField()),
                ('tiempo', models.TimeField()),
                ('nota', models.DecimalField(decimal_places=2, max_digits=2)),
                ('estudiante', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='nombre.estudiante')),
                ('quiz', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='nombre.quiz')),
            ],
        ),
    ]