from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.backends import ModelBackend
from .models import Llibre, Usuari, CD, BR, DVD, Dispositiu, Centre, Cicle
from django.views.generic import ListView
from django.db.models import Q
from .utils import generarLog,subir_logs_a_bd  # Importa la función generarLog desde utils.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import csv
from .models import Usuari
from django.contrib.auth.hashers import make_password
from datetime import datetime

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
    error_message = None  # Inicializar el mensaje de error
    usuarios_no_introducidos = []  # Inicializar la lista de usuarios no introducidos
    usuarios_agregados = 0  # Inicializar el contador de usuarios agregados exitosamente
    
    if request.method == 'POST' and request.FILES.get('archivo_csv'):
        archivo_csv = request.FILES['archivo_csv']
        nombre_centro_seleccionado = request.POST.get('nombre_centro_seleccionado')  # Obtener el nombre del centro seleccionado
        
        try:
            decoded_file = archivo_csv.read().decode('utf-8').splitlines()
            csv_reader = csv.DictReader(decoded_file)

            for row in csv_reader:
                nom = row.get('Nom')
                cognom = row.get('Cognom')
                telefon = row.get('Telefon')
                email = row.get('email')
                data_naixement = datetime.strptime(row.get('data_naixement'), '%Y-%m-%d').date()
                cicle_nom = row.get('Cicle')

                print("Leyendo fila del CSV:")
                print(f"Nombre: {nom}, Apellido: {cognom}, Teléfono: {telefon}, Email: {email}, Fecha de nacimiento: {data_naixement}, Ciclo: {cicle_nom}")

                try:
                    # Obtener o crear el ciclo
                    cicle, created = Cicle.objects.get_or_create(nom=cicle_nom)  

                    # Obtener el centro seleccionado
                    centro_seleccionado = Centre.objects.get(nom=nombre_centro_seleccionado)

                    # Crear el usuario con los datos del CSV y el centro seleccionado
                    user, created = Usuari.objects.get_or_create(
                        email=email,
                        defaults={
                            'first_name': nom,
                            'last_name': cognom,
                            'username': email,
                            'telefon': telefon,
                            'cicle': cicle,
                            'centre': centro_seleccionado,
                            'data_naixement': data_naixement,
                            'password': make_password('P@ssw0rd987'),
                            'rol': 'Alumne',
                        }
                    )
                    
                    if created:
                        usuarios_agregados += 1  # Incrementar el contador de usuarios agregados
                        print(f"Usuario '{nom} {cognom}' creado correctamente.")
                    else:
                        # Si el usuario ya existe, añadirlo a la lista de usuarios no introducidos
                        usuarios_no_introducidos.append(user)
                        print(f"El usuario '{nom} {cognom}' ya existe en la biblioteca.")
                    
                except Exception as e:
                    # Manejar cualquier error que ocurra durante la creación del usuario
                    username = row.get('Nom')  # Obtener el nombre del usuario que causó el error
                    error_message = f"No se pudo crear el usuario '{username}' debido a que ya está en la biblioteca"
                    generarLog(request, 'ERROR', f"No se pudo crear el usuario '{username}' {e}")

        except Exception as e:
            # Manejar cualquier error que ocurra durante la lectura del archivo CSV
            error_message = f"No se pudo leer el archivo CSV"
            print(error_message)
            generarLog(request, 'ERROR', f"No se pudo leer el archivo CSV: {e}")
            
    # Obtener todos los centros para pasarlos a la plantilla
    centros = Centre.objects.all()

    return render(request, 'importar_Users.html', {'centros': centros, 'error_message': error_message, 'usuarios_no_introducidos': usuarios_no_introducidos, 'usuarios_agregados': usuarios_agregados})
