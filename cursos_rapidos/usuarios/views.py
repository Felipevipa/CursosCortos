from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrarUsuarioForm

# Create your views here.
def login_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
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