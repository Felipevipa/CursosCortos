from django.urls import path
from . import views

urlpatterns = [
    path('login_user/', views.login_user, name="login"),
    path('login_user_camera/', views.login_user_camera, name="loginCamera"),
    path('logout_user', views.logout_user, name="logout"),
    # path('register_user', views.register_user, name="register-user"),
    path('registrar_estudiante', views.registrar_estudiante, name="registrar-estudiante"),
    path('registrar_docente', views.registrar_docente, name="registrar-docente"),
]
