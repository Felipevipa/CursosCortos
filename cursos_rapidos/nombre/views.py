from django.shortcuts import render, redirect, get_object_or_404
from .models import Estudiante, Carrera, Materia, Tematica, Material
from .forms import RawStudentForm, CarreraForm, MateriaForm, TematicaForm
from django.http import HttpResponseRedirect
from datetime import datetime
import os


def agregar_tematica(request, carrera, materia):
	submitted = False
	if request.method == 'POST':
		form = TematicaForm(request.POST)
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
	context = {
		'tematica': tematica,
		'material_list': material_list,
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

	print(material_list)
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


def usuario(request, id):
    obj = Estudiante.objects.get(codigo=id) #list of objects
    
    context = {
        "object": obj,
    }
    return render(request, "nombre/index.html", context)


def registro(request):
	student_form = RawStudentForm()
	if request.method == "POST":
		student_form = RawStudentForm(request.POST, request.FILES)
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

