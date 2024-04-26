from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.backends import ModelBackend
from .models import Llibre, Usuari, CD, BR, DVD, Dispositiu
from django.views.generic import ListView
from django.db.models import Q
from .utils import generarLog,subir_logs_a_bd  # Importa la función generarLog desde utils.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import csv
from .models import Usuari
from django.contrib.auth.hashers import make_password

@login_required
def dashboard(request):
    users = Usuari.objects.all()
    if request.method == "POST":
        user_id = request.POST.get('id')

        if user_id:
            try:
                usuario = Usuari.objects.get(pk=user_id)  # Cambio aquí
                usuario.username = request.POST.get('username', usuario.username)  # También aquí
                usuario.save()
                messages.success(request, 'Datos actualizados correctamente')
                generarLog(request, 'INFO', f"Datos actualizados correctamente")
                subir_logs_a_bd(request)
                return redirect('dashboard')
            except Usuari.DoesNotExist:  # Cambio aquí
                messages.error(request, 'El usuario no existe')
                generarLog(request, 'ERROR', f"El usuario no existe")
                subir_logs_a_bd(request)
                return redirect('dashboard')
        else:
            messages.error(request, 'Falta el campo ID')
            generarLog(request, 'ERROR', f"Falta el campo ID")
            subir_logs_a_bd(request)

            return redirect('dashboard')

    return render(request, 'dashboard.html', {'users': users})


def index(request):
    books = Llibre.objects.all()
    cds =  CD.objects.all()
    dvds = DVD.objects.all()
    brs = BR.objects.all()
    dispositius = Dispositiu.objects.all()

    all_items = list(books) + list(cds) + list(dvds) + list(brs) + list(dispositius)
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            # Validar la contraseña
            validate_password(password)
        except ValidationError as error:
            # Si la contraseña no cumple con los requisitos, mostrar un mensaje de error
            messages.error(request, "{}".format(", ".join(error.messages)))
            generarLog(request, 'ERROR', f"Contraseña inválida: {', '.join(error.messages)}")
            subir_logs_a_bd(request)
            return redirect('index')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            generarLog(request, 'INFO', f"Inicio de sesión correcto.")
            subir_logs_a_bd(request)
            return redirect('dashboard')  
        else:
            messages.error(request, "Correo electrónico o contraseña inválidos.")
            generarLog(request, 'ERROR', f"El correo electrónico o contraseña son inválidos.")
            subir_logs_a_bd(request)
            return redirect('index')  
    return render(request, 'index.html', {"books":all_items})




def search_results(request):
    generarLog(request, 'INFO', f"BUSQUEDA REALIZADA")
    subir_logs_a_bd(request)
    if request.method == "GET":
        query = request.GET.get("searcher")
        books = Llibre.objects.filter(
            Q(nom__icontains=query)
        )
        # Filtrar CDs
        cds = CD.objects.filter(
            Q(nom__icontains=query)
        )
        
        # Filtrar DVDs
        dvds = DVD.objects.filter(
            Q(nom__icontains=query)
        )
        
        # Filtrar Blu-rays
        brs = BR.objects.filter(
            Q(nom__icontains=query)
        )
        
        # Filtrar dispositivos
        dispositivos = Dispositiu.objects.filter(
            Q(nom__icontains=query)
        )
        return render(request, 'search_results.html', {
            'books': books,
            'cds': cds,
            'dvds': dvds,
            'brs': brs,
            'dispositivos': dispositivos,
        })

def logout_user(request):
    logout(request)
    messages.success(request, 'Has tancat la sessió')
    generarLog(request, 'INFO', f"LOGOUT.")
    subir_logs_a_bd(request)
    return redirect('index')

def importar_Users(request):
    if request.method == 'POST' and request.FILES['archivo_csv']:
        archivo_csv = request.FILES['archivo_csv']
        if archivo_csv.name.endswith('.csv'):
            try:
                decoded_file = archivo_csv.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                for row in reader:
                    nuevo_usuario = Usuari(
                        nombre=row['nombre'],
                        apellido=row['apellido'],
                        telefono=row['telefono'],
                        centro=row['centro'],
                        email=row['mail'],
                        fecha_nacimiento=row['fecha_nacimiento'],
                        contraseña=make_password('password123'),
                        rol='Alumne'
                    )
                    nuevo_usuario.save()
                
                # Renderiza la misma página HTML después de procesar el archivo
                return render(request, 'importar_Users.html', {'success_message': 'Usuarios importados correctamente.'})
            except Exception as e:
                # Llama a la función generarLog para registrar el error
                generarLog(request, 'Error', f'Error al procesar el archivo CSV: {str(e)}')
                return render(request, 'importar_Users.html', {'error_message': 'Error al procesar el archivo. Consulta los registros para más detalles.'})
        else:
            return render(request, 'importar_Users.html', {'error_message': 'Formato de archivo no válido. Se requiere un archivo CSV.'})
    
    return render(request, 'importar_Users.html')