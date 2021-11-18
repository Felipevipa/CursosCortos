from django.urls import path
from . import views

urlpatterns = [
    path('login_user/', views.login_user, name="login"),
    path('logout_user', views.logout_user, name="logout"),
    path('register_user', views.register_user, name="register-user"),
    path('registrar_estudiante', views.registrar_estudiante, name="registrar-estudiante"),
]
