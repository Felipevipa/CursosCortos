from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from nombre.models import EstudianteProfile, DocenteProfile


class RegistroDocente(forms.ModelForm):
	class Meta:
		model = DocenteProfile
		exclude = ['user']

		labels = {
			'foto': 'Foto de Perfil',
			'documento': '',
			'fechadenacimiento': 'Fecha De Nacimiento:',
		}
		widgets = {
			'foto': forms.FileInput(attrs = {'class': 'form-control',}),
			'documento': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Documento'}),
			'fechadenacimiento': forms.DateInput(attrs = {'class': 'form-control', 'placeholder': 'Fecha de Nacimiento', 'type': 'date',}),
		}



class RegistroEstudiante(forms.ModelForm):
	class Meta:
		model = EstudianteProfile
		exclude = ['user']

		labels = {
			'foto': 'Foto de Perfil',
			'codigo': '',
			'documento': '',
			'fechadenacimiento': 'Fecha De Nacimiento:',
			'carrera':'Carrera:',
		}
		widgets = {
			'foto': forms.FileInput(attrs = {'class': 'form-control',}),
			'codigo': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Codigo'}),
			'documento': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Documento'}),
			'fechadenacimiento': forms.DateInput(attrs = {'class': 'form-control', 'placeholder': 'Fecha de Nacimiento', 'type': 'date',}),
			'carrera': forms.Select(attrs={'class':'form-select',}),
		}


class RegistrarUsuarioForm(UserCreationForm):
	email = forms.EmailField(widget=forms.EmailInput(attrs={
			'class': 'form-control'
		}))
	first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
			'class': 'form-control'
		}))
	last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
			'class': 'form-control'
		}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


	def __init__(self, *args, **kwargs):
		super(RegistrarUsuarioForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['class'] = 'form-control'
