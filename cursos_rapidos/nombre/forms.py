from django import forms
import datetime
from .models import Estudiante, Carrera, Materia, Tematica


class TematicaForm(forms.ModelForm):

	

	class Meta:
		model = Tematica
		fields = '__all__'
		labels = {
			'imagen': 'Portada',
			'titulo': '',
			'resumen': '',
			'materia': 'Materia:',
			'docente':'Docente:',
			'is_available': 'Disponible',
		}
		widgets = {
			'imagen': forms.FileInput(attrs = {'class': 'form-control',}),
			'titulo': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Titulo de la Tematica'}),
			'resumen': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Resumen de la Tematica','rows':3,}),
			'materia': forms.Select(attrs={'class':'form-select', 'readonly': True,}),
			'docente': forms.Select(attrs={'class':'form-select',}),
			# 'is_available': forms.NullBooleanField(attrs={'class':'form-select',}),
		}



class MateriaForm(forms.ModelForm):
	class Meta:
		model = Materia
		fields = '__all__'
		labels = {
			'nombre': '',
			'carrera': 'Carrera:',
		}
		widgets = {
			'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre de la materia'}),
			'carrera': forms.Select(attrs={'class':'form-select', 'readonly': True,}),
		}


class CarreraForm(forms.ModelForm):
	class Meta:
		model = Carrera
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

	carrera = forms.ModelChoiceField(queryset = Carrera.objects.all(), widget=forms.Select(
		attrs = {
			'class': 'form-control',
		}
	))
	

	class Meta:
		model = Estudiante
		fields = '__all__'