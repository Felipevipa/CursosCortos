from django.urls import path
from proyectowebapp import views


urlpatterns = [
  
    path('',views.index,name="Index"),
    path('index.html',views.index,name="Index"),
    path('tab-panel.html',views.tab,name="tab"),
    path('chart.html',views.chart,name= "chart"),
    path('table.html',views.table,name="table" ),
]