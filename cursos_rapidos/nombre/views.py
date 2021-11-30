from django.shortcuts import render, redirect, get_object_or_404
from .models import EstudianteProfile, Carrera, Materia, Tematica, Material, Quiz
from .forms import RawStudentForm, CarreraForm, MateriaForm, TematicaForm, MaterialForm
from django.http import HttpResponseRedirect
from datetime import datetime
# from . import version_aplicable
import os
from django.views.decorators.clickjacking import xframe_options_exempt
import re



@xframe_options_exempt
def preguntar(request):
	if request.method == 'POST':
		pregunta = request.POST['pregunta']
		print(pregunta)
		respuesta = "Respuesta"

		if request.user.groups.filter(name="Estudiantes").exists():
  			respuesta = "Acceso concedido"
		# respuesta = version_aplicable.pregunta_respuesta_escrito(pregunta)
		context = {
			'pregunta': pregunta,
			'respuesta': respuesta,
		}
		return render(request, "nombre/preguntar.html", context)

	else:
		context = {

		}
		return render(request, "nombre/preguntar.html", context)



def calificaciones(request):
	print(request.user.groups.filter(name="Estudiantes").exists())
	obj = EstudianteProfile.objects.get(user=request.user) 
	calificaciones = Calificacion.objects.filter(estudiante=obj)
	for calificacion in calificaciones:
		valor=calificacion.nota
		print(valor)
	
	context = {"object": obj,
				"calificaciones": calificaciones}
	return render(request, 'nombre/calificaciones.html', context)
	


def quiz(request, carrera, materia, tematica, id):
	carrera = get_object_or_404(Carrera, nombre=carrera)
	materia = get_object_or_404(Materia, carrera=carrera, nombre=materia)
	tematica = get_object_or_404(Tematica, materia=materia, titulo=tematica)
	#quiz = get_object_or_404(Quiz, tematica=tematica, id=id)
	quiz = Quiz.objects.filter(id=id)
	print(quiz)
	context = {
		'quiz': quiz,
	}
	return render(request, "nombre/quiz.html", context)

	

def agregar_material(request, carrera, materia, tematica):
	submitted = False
	if request.method == 'POST':
		form = MaterialForm(request.POST, request.FILES)
		print('EL FORMULARIO ES VALIDO' + str(form.is_valid()))
		if form.is_valid():
			tematica = Tematica.objects.get(titulo=tematica)
			material = form.save(commit=False)
			material.tematica = tematica# material.video = re.sub(r"(?ism).*?=(.*?)$", r"https://www.youtube.com/embed/\1", material.video)
			print(material.video)
			if material.video != None:
				material.video = re.split(r"(?ism).*?=(.*?)$", material.video)
				material.video = material.video[1][0:material.video[1].index('&')]
			material.save()
			next = request.POST.get('next', '/')
			return HttpResponseRedirect(next)
			# return redirect('home')
	else:
		form = MaterialForm()
		if 'submitted' in request.GET:
			submitted = True

	context = {
		'form': form,
		'submitted': submitted,
	}
	return render(request, 'nombre/agregar_material.html', context)



def agregar_tematica(request, carrera, materia):
	submitted = False
	if request.method == 'POST':
		form = TematicaForm(request.POST, request.FILES)
		print('EL FORMULARIO ES VALIDO' + str(form.is_valid()))
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('?submitted=True')
	else:
		materia = Materia.objects.get(nombre=materia)
		form = TematicaForm(initial={'materia': materia})
		if 'submitted' in request.GET:
			submitted = True

	context = {
		'form': form,
		'submitted': submitted,
	}
	return render(request, 'nombre/agregar_tematica.html', context)	



def actualizar_materia(request, carrera, materia_id):
	materia = Materia.objects.get(pk=materia_id)
	form = MateriaForm(request.POST or None, instance=materia)
	if form.is_valid():
		form.save()
		return redirect('ver-carrera', carrera)
	context = {
		'materia': materia,
		'form': form,
		'page_title': "Actualizar Materia",
	}
	return render(request, 'nombre/actualizar_materia.html', context)


def actualizar_tematica(request, carrera, materia, tematica_id):
	tematica = Tematica.objects.get(pk=tematica_id)
	form = TematicaForm(request.POST or None, instance=tematica)
	if form.is_valid():
		form.save()
		return redirect('ver-materia', carrera, materia)

	context = {
		'carrera': carrera,
		'materia': materia,
		'form': form,
		'page_title': "Actualizar Tematica",
	}

	return render(request, 'nombre/actualizar_tematica.html', context)


def eliminar_tematica(request, carrera, materia, tematica_id):
	tematica = Tematica.objects.get(pk=tematica_id)
	tematica.delete()
	return redirect('ver-materia', carrera, materia)


def eliminar_materia(request, carrera, materia_id):
	materia = Materia.objects.get(pk=materia_id)
	materia.delete()
	return redirect('ver-carrera', carrera)


def eliminar_carrera(request, carrera_id):
	carrera = Carrera.objects.get(pk=carrera_id)
	carrera.delete()
	return redirect('carreras-detail')


def agregar_materia(request, carrera):
	submitted = False
	if request.method == 'POST':
		form = MateriaForm(request.POST)
		
		if form.is_valid():
			form.save()
			print(carrera)
			return HttpResponseRedirect('?submitted=True')
	else:
		carrera = Carrera.objects.get(nombre=carrera)
		# form = MateriaForm({'carrera': carrera})
		form = MateriaForm(initial={'carrera': carrera})
		if 'submitted' in request.GET:
			submitted = True

	context = {
		'form': form,
		'submitted': submitted,
	}
	return render(request, 'nombre/agregar_materia.html', context)



def actualizar_carrera(request, carrera_id):
	carrera = Carrera.objects.get(pk=carrera_id)
	form = CarreraForm(request.POST or None, instance=carrera)
	if form.is_valid():
		form.save()
		return redirect('carreras-detail')
	context = {
		'carrera': carrera,
		'form': form,
		'page_title': "Actualizar Carrera",
	}
	return render(request, 'nombre/actualizar_carrera.html', context)


def agregar_carrera(request):
	submitted = False
	if request.method == 'POST':
		form = CarreraForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/agregar_carrera?submitted=True')
	else:
		form = CarreraForm
		if 'submitted' in request.GET:
			submitted = True

	context = {
		'form': form,
		'submitted': submitted,
	}
	return render(request, 'nombre/agregar_carrera.html', context)



def search_tematica(request):
	context = {
	}
	if request.method == 'POST':
		searched = request.POST['searched']
		tematicas = Tematica.objects.filter(titulo__contains=searched)
		material_list = []
		for tematica in tematicas:
			material = Material.objects.filter(tematica=tematica)
			for mater in material:
				material_list.append((tematica.titulo, mater))


		context = {
			'searched': searched,
			'tematicas': tematicas,
			'material_list': material_list,
		}

	
	return render(request, 'nombre/search_tematica.html', context)


def ver_tematica(request, carrera, materia, titulo):
	carrera = get_object_or_404(Carrera, nombre=carrera)
	materia = get_object_or_404(Materia, carrera=carrera, nombre=materia)
	tematica = get_object_or_404(Tematica, materia=materia, titulo=titulo)
	material_list = Material.objects.filter(tematica=tematica)
	quizes = Quiz.objects.filter(tematica=tematica)
	form = MaterialForm()
	context = {
		'tematica': tematica,
		'material_list': material_list,
		'form': form,
		'quizes': quizes,
	}
	return render(request, "nombre/ver_tematica.html", context)


def ver_materia(request, carrera, nombre):
	# obj = Carrera.objects.get(nombre=nombre)
	carrera = get_object_or_404(Carrera, nombre=carrera)
	materia = get_object_or_404(Materia, carrera=carrera, nombre=nombre)
	tematicas_list = Tematica.objects.filter(materia=materia)
	material_list = []
	for tematica in tematicas_list:
		material = Material.objects.filter(tematica=tematica)
		for mater in material:
			print(mater)
			material_list.append((tematica.titulo, mater))


	context = {
		'materia': materia,
		'tematicas_list': tematicas_list,
		'material_list': material_list,
	}
	return render(request, "nombre/ver_materia.html", context)


def ver_carrera(request, nombre):
	# obj = Carrera.objects.get(nombre=nombre)
	carrera = get_object_or_404(Carrera, nombre=nombre)
	materias_list = Materia.objects.filter(carrera=carrera)
	context = {
		'carrera': carrera,
		'materias_list': materias_list,
	}
	return render(request, "nombre/ver_carrera.html", context)


def carreras_view(request):
	carrera_list = Carrera.objects.all().order_by('nombre')
	context = {
		'carrera_list': carrera_list,
		'page_title': "Carreras",
    }
	return render(request, "nombre/carreras_list.html", context)


def usuario(request):
	print(request.user.groups.filter(name="Estudiantes").exists())
	obj = EstudianteProfile.objects.get(user=request.user) 
	context = {"object": obj,}
	return render(request, "nombre/ver_perfil.html", context)



def registro(request):
	student_form = RawStudentForm()
	if request.method == "POST":
		student_form = RawStudentForm(request.POST, request.FILES)
		print('EL FORMULARIO ES VALIDO' + str(student_form.is_valid()))
		if student_form.is_valid():
			student_form.save()
			return redirect("registro")
		else:
			context = {
				'form': student_form
			}
			return render(request, 'nombre/registro.html', context)


	

	context = {
		'form': student_form,
		'tiempo': datetime.now()
	}

	
	return render(request, 'nombre/registro.html', context)

def home(request):
	cursos = Tematica.objects.filter(is_available=True).order_by('-last_updated')
	material_list = []
	for curso in cursos:
		material = Material.objects.filter(tematica=curso)
		for mater in material:	

			material_list.append((curso.titulo, mater))

	context = {
		'cursos': cursos,
		'material_list': material_list,
		'page_title': "UGC",
		}
	return render(request, 'nombre/home.html', context)

	