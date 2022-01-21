from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from nombre.models import EstudianteProfile, DocenteProfile
from .forms import RegistrarUsuarioForm, RegistroEstudiante, RegistroDocente
import base64
from PIL import Image
import numpy as np
import io

# Create your views here.
def login_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			if request.user.groups.filter(name="Estudiantes").exists():
				request.session['foto'] = EstudianteProfile.objects.get(user=user).foto.url
			if request.user.groups.filter(name="Docentes").exists():
				request.session['foto'] = DocenteProfile.objects.get(user=user).foto.url
			return redirect('home')


		else:
			messages.success(request, ("No fue posible ingresar, intente nuevamente..."))
			return redirect('login')

	else:
		context = {

		}
		return render(request, 'autenticacion/login.html', context)


def login_user_camera(request):
	if request.method == 'POST':
		username = request.POST['username']
		photo = request.POST['photo']
		print(username)
		print("foto: ")
		print(type(photo))
		print(photo)
		photo = photo[22:len(photo)]
		base64_decoded = base64.b64decode(photo)
		image = Image.open(io.BytesIO(base64_decoded))
		image_np = np.array(image)
		print(image_np)
		user = User.objects.get(username=username)
		login(request, user)
		if request.user.groups.filter(name="Estudiantes").exists():
			request.session['foto'] = EstudianteProfile.objects.get(user=user).foto.url
		if request.user.groups.filter(name="Docentes").exists():
			request.session['foto'] = DocenteProfile.objects.get(user=user).foto.url
		return redirect('home')

def logout_user(request):
	logout(request)
	messages.success(request, ("Has salido de tu cuenta"))
	return redirect('home')


def register_user(request):
	if request.method == 'POST':
		form = RegistrarUsuarioForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username,password=password)
			login(request, user)
			messages.success(request, ('Registro completo'))
			return redirect('home')
	else:
		form = RegistrarUsuarioForm()

	context = {
		'form': form,
	}
	return render(request, 'autenticacion/registrar_usuario.html', context)


def registrar_estudiante(request):
	if request.method == 'POST':
		form_user = RegistrarUsuarioForm(request.POST)
		form_profile = RegistroEstudiante(request.POST, request.FILES)
		if form_profile.is_valid() and form_user.is_valid():

			user = form_user.save()

			profile = form_profile.save(commit=False)
			profile.user = user
			profile.save()
			group = Group.objects.get(name="Estudiantes")
			user.groups.add(group)

			username = form_user.cleaned_data['username']
			password = form_user.cleaned_data['password1']
			user = authenticate(username=username,password=password)
			login(request, user)
			messages.success(request, ('Registro completo'))
			return redirect('home')
	else:
		form_profile = RegistroEstudiante()
		form_user = RegistrarUsuarioForm()

	context = {
		'form_profile': form_profile,
		'form_user': form_user,
	}
	return render(request, 'autenticacion/registrar_estudiante.html', context)



def registrar_docente(request):
	if request.user.groups.filter(name="Docentes").exists():
	
		if request.method == 'POST':
			form_user = RegistrarUsuarioForm(request.POST)
			form_profile = RegistroDocente(request.POST, request.FILES)
			if form_profile.is_valid() and form_user.is_valid():

				user = form_user.save()

				profile = form_profile.save(commit=False)
				profile.user = user
				profile.save()
				group = Group.objects.get(name="Docentes")
				user.groups.add(group)

				username = form_user.cleaned_data['username']
				password = form_user.cleaned_data['password1']
				user = authenticate(username=username,password=password)
				login(request, user)
				messages.success(request, ('Registro completo'))
				return redirect('home')
		else:
			form_profile = RegistroDocente()
			form_user = RegistrarUsuarioForm()

		context = {
			'form_profile': form_profile,
			'form_user': form_user,
		}
		return render(request, 'autenticacion/registrar_docente.html', context)

	else:
			return redirect('login_requerido')
	