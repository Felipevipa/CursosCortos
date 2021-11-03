from django.shortcuts import render,HttpResponse

def index (request):
    return render (request,("proyectowebapp/index.html"))


def tab (request):
    return render (request,("proyectowebapp/tab-panel.html"))


def chart (request):
    return render (request,("proyectowebapp/chart.html"))


def table (request):
   return render (request,("proyectowebapp/table.html"))


      
# Create your views here.
