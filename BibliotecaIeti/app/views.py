from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.backends import ModelBackend
from .utils import generarLog,subir_logs_a_bd  # Importa la función generarLog desde utils.py

def dashboard(request):
    return render(request, 'dashboard.html')

def index(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Inicio de sesión exitoso.")
            # Generar un log exitoso de inicio de sesión
            generarLog(request, 'INFO', f"Inicio de sesión exitoso")
            return redirect('index')  # Redirigir a la página principal después de iniciar sesión correctamente
        else:
            messages.error(request, "Correo electrónico o contraseña inválidos.")
            subir_logs_a_bd(request)
            # Generar un log de intento fallido de inicio de sesión
            generarLog(request, 'ERROR', f"Intento de inicio de sesión fallido")
            return redirect('index')  # Redirigir de vuelta a la página de inicio de sesión en caso de fallo
    return render(request, 'index.html')


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
