from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from nombre.models import EstudianteProfile
from .forms import RegistrarUsuarioForm, RegistroEstudiante

# Create your views here.
def login_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			request.session['foto'] = EstudianteProfile.objects.get(user=user).foto.url
			print(EstudianteProfile.objects.get(user=user).foto.url)
			return redirect('home')


		else:
			messages.success(request, ("No fue posible ingresar, intente nuevamente..."))
			return redirect('login')

	else:
		context = {

		}
		return render(request, 'autenticacion/login.html', context)


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