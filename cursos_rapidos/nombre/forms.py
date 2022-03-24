from django import forms
import datetime
from .models import *


class EnrolamientoForm(forms.ModelForm):
	class Meta:
		model = Enrolamiento
		fields = '__all__'


class CalificacionForm(forms.ModelForm):
	class Meta:
		model = Calificacion
		fields = '__all__'


class RespuestaUsuarioAbiertaForm(forms.ModelForm):
	class Meta:
		model = RespuestaUsuarioAbierta
		exclude = ['pregunta']


class PalabrasClaveRespuestaAbiertaForm(forms.ModelForm):
	class Meta:
		model = PalabrasClaveRespuestaAbierta
		exclude = {'pregunta'}
		labels = {
			'palabra': '',
		}
		widgets = {
			'palabra': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Palabra clave',}),
		}



class OpcionRespuestaAbiertaForm(forms.ModelForm):
	
	class Meta:
		model = OpcionRespuestaAbierta
		exclude = {'pregunta'}
		labels = {
			'respuesta': '',
		}
		widgets = {
			'respuesta': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Posible respuesta abierta','rows':5,}),
		}


class OpcionRespuestaCerradaForm(forms.ModelForm):
	
	class Meta:
		model = OpcionRespuestaCerrada
		exclude = {'pregunta'}
		labels = {
			'opcion_multiple': '',
		}
		widgets = {
			'opcion_multiple': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Opcion Multiple',}),
		}


class PreguntaForm(forms.ModelForm):
	
	class Meta:
		CHOICES=[('1','Opcion Multiple'),('2','Abierta')]
		model = Pregunta
		exclude = {'quiz'}
		labels = {
			'enunciado': 'Digite su pregunta',
			'answer_type': 'Tipo de respuesta',
		}
		widgets = {
			'enunciado': forms.Textarea(attrs={'class':'form-control', 'placeholder':'','rows':3,}),
			'answer_type': forms.Select(choices=CHOICES,attrs={'class':'form-control','placeholder':'Seleccione opción de respuesta',}),
		}




class QuizForm(forms.ModelForm):
	class Meta:
		model = Quiz
		exclude = ['curso']
		labels = {
			'titulo': '',
		}
		widgets = {
			'titulo': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Titulo',}),
		}


class MaterialForm(forms.ModelForm):
	class Meta:
		model = Material
		exclude = ['curso', 'quizes']
		labels = {
			'titulo': '',
			'contenido_de_texto': '',
			'imagen': 'Imagen',
			'video': '',
			'materialExterno': '',
		}
		widgets = {
			'titulo': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Titulo',}),
			'contenido_de_texto': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Contenido de Texto'}),
			'imagen': forms.FileInput(attrs = {'class': 'form-control',}),
			'video': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Link del video',}),
			'materialExterno': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Link del material externo',}),
		}


class CursoForm(forms.ModelForm):
	class Meta:
		model = Curso
		exclude = ['color1', 'color2']
		labels = {
			'imagen': 'Portada',
			'titulo': '',
			'resumen': '',
			'tematica': 'Materia:',
			'is_available': 'Disponible',
		}
		widgets = {
			'imagen': forms.FileInput(attrs = {'class': 'form-control',}),
			'titulo': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Titulo de la Tematica'}),
			'resumen': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Resumen de la Tematica','rows':3,}),
			'tematica': forms.Select(attrs={'class':'form-select', 'readonly': True,}),
			# 'is_available': forms.NullBooleanField(attrs={'class':'form-select',}),
		}



class TematicaForm(forms.ModelForm):
	class Meta:
		model = Tematica
		fields = '__all__'
		labels = {
			'nombre': '',
			'carrera': 'Carrera:',
		}
		widgets = {
			'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre de la materia'}),
			'carrera': forms.Select(attrs={'class':'form-select', 'readonly': True,}),
		}


class CategoriaForm(forms.ModelForm):
	class Meta:
		model = Categoria
		fields = '__all__'
		labels = {
			'nombre': '',
		}
		widgets = {
			'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre de la carrera'}),
		}
		




class RawStudentForm(forms.ModelForm):
	'''
	class Meta:
		model = Estudiante

		fields = ('foto', 'codigo', 'nombres', 'apellidos', 'documento', 'fechadenacimiento', 'email', 'usuario', 'contrasena', 'carrera')

		
		
		widgets = {
			'foto': forms.ImageField(required=True),
			'codigo': forms.IntegerField(required=True),
			'nombres': forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Nombres completos",})),
			'apellidos': forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Apellidos completos",})),
			'documento': forms.IntegerField(required=True),
			'fechadenacimiento': forms.DateField(required=True, input_formats=["%Y-%m-%d"]),
			'email': forms.EmailField(required=True),
			'usuario': forms.CharField(required=True, max_length=50),
			'contrasena': forms.CharField(required=True, max_length=18),
			'carrera': forms.ModelMultipleChoiceField(queryset=Carrera.objects.all()),
		}
		
	'''	
	foto = forms.ImageField(required=True, widget=forms.FileInput(
		attrs = {
			'class': 'form-control',
		}
	))

	codigo = forms.IntegerField(required=True, widget=forms.NumberInput(
		attrs = {
			'class': 'form-control',
			'placeholder': 'codigo',
		}
	))

	nombres = forms.CharField(required=True, label='Nombres Completos', widget=forms.TextInput(
		attrs = {
			'class': 'form-control',
			'placeholder': 'Nombres',
		}
	))

	apellidos = forms.CharField(required=True, label='Apellidos Completos', widget=forms.TextInput(
		attrs = {
			'class': 'form-control',
			'placeholder': 'Apellidos',
		}
	))

	documento = forms.IntegerField(required=True, widget=forms.NumberInput(
		attrs = {
			'class': 'form-control',
			'placeholder': 'Documento',
		}
	))

	fechadenacimiento = forms.DateField(required=True, widget=forms.DateInput	(
		attrs = {
			'class': 'form-control',
			'placeholder': 'Fecha de Nacimiento',
			'type': 'date',
		}
	))

	email = forms.EmailField(required=True, widget=forms.EmailInput(
		attrs = {
			'class': 'form-control',
			'placeholder': 'email@email.com',
		}
	))

	usuario = forms.CharField(required=True, widget=forms.TextInput(
		attrs = {
			'class': 'form-control',
			'placeholder': 'usuario',
		}
	))

	password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(
		attrs = {
			'class': 'form-control',
			'placeholder': 'Ingrese su contraseña...',
		}
	))

	categoria = forms.ModelChoiceField(queryset = Categoria.objects.all(), widget=forms.Select(
		attrs = {
			'class': 'form-control',
		}
	))
	

	class Meta:
		model = UserProfile
		fields = '__all__'