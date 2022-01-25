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
import requests
import os
from io import BytesIO



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
		# print(username)
		# print("foto: ")
		# print(type(photo))
		# print(photo)
		foto2 = photo[22:len(photo)]


		user = User.objects.get(username=username)
		if user.groups.filter(name="Estudiantes").exists():
			foto1 = EstudianteProfile.objects.get(user=user).foto.url
		if user.groups.filter(name="Docentes").exists():
			foto1 = DocenteProfile.objects.get(user=user).foto.url

		# foto1 = Image.open(R"media\static\images\estudiantes\yeisonfoto.jpg")
		foto1 = Image.open(foto1[1:])

		output_buffer = BytesIO()
		foto1.save(output_buffer, format='JPEG')
		byte_data = output_buffer.getvalue()
		foto1 = base64.b64encode(byte_data)
		foto1 = foto1.decode("utf-8")

		url = 'http://127.0.0.1:6000/reconocimiento'
		apiContext = {'foto1': foto1,
					  'foto2': foto2}

		r = requests.post(url, json = apiContext)

		print(r.status_code)

		if r.status_code == 200:
			data = r.json()
			print(data)

			if data["identificacion"] == 1:
				login(request, user)
				if request.user.groups.filter(name="Estudiantes").exists():
					request.session['foto'] = EstudianteProfile.objects.get(user=user).foto.url
				if request.user.groups.filter(name="Docentes").exists():
					request.session['foto'] = DocenteProfile.objects.get(user=user).foto.url
				return redirect('home')
				
		messages.success(request, ("No fue posible ingresar, intente nuevamente..."))
		return redirect('login')


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
	