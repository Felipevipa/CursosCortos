from django.shortcuts import render, redirect, get_object_or_404
from .models import EstudianteProfile, DocenteProfile, Carrera, Materia, Tematica, Material, Quiz, Calificacion, Pregunta, OpcionRespuestaCerrada
from .forms import *
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from datetime import datetime
import time
# from . import version_aplicable
import os
from django.views.decorators.clickjacking import xframe_options_exempt
# import re
import requests



@xframe_options_exempt
def preguntar(request):
	if request.method == 'POST':
		pregunta = request.POST['pregunta']
		print(pregunta)
		url = 'http://127.0.0.1:4000/preguntas'
		apiContext = {'pregunta': pregunta}

		r = requests.post(url, json = apiContext)

		print(r.status_code)

		if r.status_code == 200:
			data = r.json()
			print(type(data))
			respuesta = data["pregunta"][0]["respuesta"]
			print(data)

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
	calificaciones = Calificacion.objects.filter(estudiante=obj).order_by('-fecha')
	for calificacion in calificaciones:
		valor = calificacion.nota
	
	context = {"object": obj,
				"calificaciones": calificaciones}
	return render(request, 'nombre/calificaciones.html', context)


def calificaciones_chart(request):
	estudiante = EstudianteProfile.objects.get(user=request.user)
	calificaciones = Calificacion.objects.filter(estudiante=estudiante).order_by('-nota')

	labels = []
	data = []

	for calificacion in calificaciones:
		labels.append(calificacion.quiz.titulo)
		data.append(calificacion.nota)

	return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
	


def quiz(request, carrera, materia, tematica, id):
	quiz = Quiz.objects.get(pk=id)
	if request.method == 'POST':
		preguntas = Pregunta.objects.filter(quiz=quiz)
		acum = 0
		for pregunta in preguntas:
			if pregunta.answer_type == '1':
				respuestaEstudiante = request.POST[str(pregunta.id)]
				respuestaPregunta = OpcionRespuestaCerrada.objects.get(pregunta=pregunta, respuesta_correcta=True)

				acum += respuestaEstudiante == respuestaPregunta.opcion_multiple

			if pregunta.answer_type == '2':
				respuestaEstudiante = request.POST[str(pregunta.id)]
				form = RespuestaEstudianteAbiertaForm()
				respuestaAbierta = form.save(commit=False)
				respuestaAbierta.respuesta = respuestaEstudiante
				respuestaAbierta.pregunta = pregunta
				respuestaAbierta.estudianteProfile = EstudianteProfile.objects.get(user=request.user)
				respuestaAbierta.save()
				print(respuestaEstudiante)


		nota = acum * (50/len(preguntas))
		current_time = datetime.now().strftime("%H:%M:%S")
		tiempo = datetime.strptime(current_time, '%H:%M:%S') - datetime.strptime(request.session['tiempoquiz'], '%H:%M:%S')

		form = CalificacionForm()
		calificacion = form.save(commit=False)
		calificacion.fecha = datetime.now()
		calificacion.tiempo = str(tiempo)
		calificacion.nota = nota
		calificacion.quiz = quiz
		calificacion.estudiante = EstudianteProfile.objects.get(user=request.user)
		calificacion.save()

		return redirect("calificaciones")



	if str(quiz.tematica.id)  == tematica and  quiz.tematica.materia.nombre == materia and quiz.tematica.materia.carrera.nombre == carrera:
		preguntas = Pregunta.objects.filter(quiz=quiz)
		opcionesRespuesta = []
		for pregunta in preguntas:
			if pregunta.answer_type == '1':
				opcionesRespuesta.append((pregunta, OpcionRespuestaCerrada.objects.filter(pregunta=pregunta).order_by('?')))
			elif pregunta.answer_type == '2':
				opcionesRespuesta.append((pregunta, 'abierta'))
		context = {
			'quiz': quiz,
			'opcionesRespuesta': opcionesRespuesta,
		}
		request.session['tiempoquiz'] = datetime.now().strftime("%H:%M:%S")

		return render(request, "nombre/quiz.html", context)

	else: 
		return HttpResponseNotFound()




def agregar_pregunta(request, carrera, materia, tematica, quiz):
	if request.user.groups.filter(name="Docentes").exists():
		submitted = False
		if request.method == 'POST':
			form = PreguntaForm(request.POST)
			if form.is_valid():
				#form.save()
				quiz = Quiz.objects.get(pk=quiz)
				pregunta= form.save(commit=False)
				pregunta.quiz=quiz
				pregunta.save()
				# return HttpResponseRedirect('home')
				return redirect('quiz', carrera, materia, tematica, quiz.id)
		else:
			form = PreguntaForm()
			if 'submitted' in request.GET:
				submitted = True

		context = {
			'form': form,
			'submitted': submitted,
		}
		return render(request, 'nombre/agregar_pregunta.html', context)
	else:
		return redirect('login_requerido')



def agregar_respuesta(request, carrera, materia, tematica, quiz, pregunta):
	submitted = False
	pregunta = Pregunta.objects.get(pk=pregunta)
	answer_type = pregunta.answer_type
	if request.method == 'POST':
		if answer_type == "1":
			form = OpcionRespuestaCerradaForm(request.POST)
		elif answer_type == "2":
			form = OpcionRespuestaAbiertaForm(request.POST)
		
		if form.is_valid():
			#form.save()
			agregar_respuesta= form.save(commit=False)
			agregar_respuesta.pregunta=pregunta
			agregar_respuesta.save() 
			print(pregunta)
			# return HttpResponseRedirect('home')
			return redirect('quiz', carrera, materia, tematica, quiz)
	else:
		if answer_type == "1":
			form = OpcionRespuestaCerradaForm()
		elif answer_type == "2":
			form = OpcionRespuestaAbiertaForm()
		if 'submitted' in request.GET:
			submitted = True

	context = {
		'form': form,
		'submitted': submitted,
	}
	return render(request, 'nombre/agregar_respuesta.html', context)




def agregar_quiz(request, carrera, materia, tematica):
	if request.user.groups.filter(name="Docentes").exists():
		submitted = False
		if request.method == 'POST':
			form = QuizForm(request.POST)
			if form.is_valid():
				tematica = Tematica.objects.get(pk=tematica)
				quiz = form.save(commit=False)
				quiz.tematica = tematica
				quiz.save()
				material = Material.objects.create()
				material.tematica = tematica
				material.quizes = quiz

				material.save()
				print(quiz.id)
				# return HttpResponseRedirect('home')
				return redirect('quiz', carrera, materia, tematica.id, quiz.id)

		else:
			form = QuizForm()
			if 'submitted' in request.GET:
				submitted = True

		context = {
			'form': form,
			'submitted': submitted,
		}
		return render(request, 'nombre/agregar_quiz.html', context)
	else:
		return redirect('login_requerido')




def agregar_material(request, carrera, materia, tematica):
	if request.user.groups.filter(name="Docentes").exists():
		submitted = False
		if request.method == 'POST':
			form = MaterialForm(request.POST, request.FILES)
			print('EL FORMULARIO ES VALIDO' + str(form.is_valid()))
			if form.is_valid():
				tematica = Tematica.objects.get(pk=tematica)
				material = form.save(commit=False)
				material.tematica = tematica# material.video = re.sub(r"(?ism).*?=(.*?)$", r"https://www.youtube.com/embed/\1", material.video)
				print(material.video)
				if material.video != None:
					material.video += "&"
					material.video = re.split(r"(?ism).*?=(.*?)$", material.video)
					material.video = material.video[1][0:material.video[1].index('&')]
				material.save()
				return redirect('ver-tematica', carrera, materia, tematica.id)
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
	else:
		return redirect('login_requerido')


def actualizar_material(request, carrera, materia, tematica, id):
	if request.user.groups.filter(name="Docentes").exists():
		material = Material.objects.get(pk=id)
		form = MaterialForm(request.POST or None, instance=material)
		if form.is_valid():
			form.save()
			return redirect('ver-tematica', carrera, materia, tematica)
		context = {
			'material': material,
			'form': form,
			'page_title': "Actualizar Material",
		}
		return render(request, 'nombre/actualizar_material.html', context)
	else:
		return redirect('login_requerido')


def eliminar_material(request, carrera, materia, tematica, id):
	if request.user.groups.filter(name="Docentes").exists():
		material = Material.objects.get(pk=id)
		material.delete()
		return redirect('ver-tematica', carrera, materia, tematica)
	else:
		return redirect('login_requerido')



def agregar_tematica(request, carrera, materia):
	if request.user.groups.filter(name="Docentes").exists():

		submitted = False
		if request.method == 'POST':
			print(request.POST['tematicaColor1'])
			print(request.POST['tematicaColor2'])
			form = TematicaForm(request.POST, request.FILES)
			if form.is_valid():
				tematica = form.save(commit=False)
				tematica.color1 = request.POST['tematicaColor1']
				tematica.color2 = request.POST['tematicaColor2']
				tematica.save()				
				return HttpResponseRedirect('?submitted=True')
		else:
			materia = Materia.objects.get(nombre=materia)
			form = TematicaForm(initial={'materia': materia})
			if 'submitted' in request.GET:
				submitted = True

		context = {
			'form': form,
			'submitted': submitted,
			'page_title': "Agregar Tematica",

		}
		return render(request, 'nombre/agregar_tematica.html', context)	
	else:
		return redirect('login_requerido')


def actualizar_materia(request, carrera, materia_id):
	if request.user.groups.filter(name="Docentes").exists():
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
	else:
		return redirect('login_requerido')


def actualizar_tematica(request, carrera, materia, tematica_id):
	if request.user.groups.filter(name="Docentes").exists():
		tematica = Tematica.objects.get(pk=tematica_id)
		form = TematicaForm(request.POST or None, instance=tematica)
		if form.is_valid():
			tematica = form.save(commit=False)
			tematica.color1 = request.POST['tematicaColor1']
			tematica.color2 = request.POST['tematicaColor2']
			tematica.save()		
			return redirect('ver-materia', carrera, materia)


		context = {
			'carrera': carrera,
			'materia': materia,
			'form': form,
			'page_title': "Actualizar Tematica",

		}

		return render(request, 'nombre/agregar_tematica.html', context)
	else:
		return redirect('login_requerido')


def eliminar_tematica(request, carrera, materia, tematica_id):
	if request.user.groups.filter(name="Docentes").exists():
		tematica = Tematica.objects.get(pk=tematica_id)
		tematica.delete()
		return redirect('ver-materia', carrera, materia)
	else:
		return redirect('login_requerido')


def eliminar_materia(request, carrera, materia_id):
	if request.user.groups.filter(name="Docentes").exists():
		materia = Materia.objects.get(pk=materia_id)
		materia.delete()
		return redirect('ver-carrera', carrera)
	else:
		return redirect('login_requerido')


def eliminar_carrera(request, carrera_id):
	if request.user.groups.filter(name="Docentes").exists():
		carrera = Carrera.objects.get(pk=carrera_id)
		carrera.delete()
		return redirect('carreras-detail')
	else:
		return redirect('login_requerido')


def agregar_materia(request, carrera):
	if request.user.groups.filter(name="Docentes").exists():
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
	else:
		return redirect('login_requerido')



def actualizar_carrera(request, carrera_id):
	if request.user.groups.filter(name="Docentes").exists():
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
	else:
		return redirect('login_requerido')


def agregar_carrera(request):
	if request.user.groups.filter(name="Docentes").exists():
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
	else:
		return redirect('login_requerido')



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


def ver_tematica(request, carrera, materia, id):
	tematica = get_object_or_404(Tematica, pk=id)
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
	if request.user.groups.filter(name="Estudiantes").exists():
		obj = EstudianteProfile.objects.get(user=request.user)
	if request.user.groups.filter(name="Docentes").exists():
		obj = DocenteProfile.objects.get(user=request.user) 
	context = {"object": obj,}
	return render(request, "nombre/ver_perfil.html", context)


def home(request):
	cursos = Tematica.objects.filter(is_available=True).order_by('-last_updated')

	context = {
		'cursos': cursos,
		'page_title': "Aprendapp",
		}
	return render(request, 'nombre/home.html', context)

def login_requerido(request):
	context = {}
	return render(request, 'nombre/login_requerido.html', context)

	