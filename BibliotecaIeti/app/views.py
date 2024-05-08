from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.backends import ModelBackend
from .models import Llibre, Usuari, CD, BR, DVD, Dispositiu, Centre, Cicle, Prestec,Catalog, Reserva,ElementCatalog
from django.views.generic import ListView
from django.db.models import Q
from .utils import generarLog,subir_logs_a_bd  # Importa la función generarLog desde utils.py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.password_validation import validate_password
from datetime import datetime
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from .decorators import check_user_able_to_see_page
from .forms import UserRegisterForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.hashers import make_password
import csv
from .models import Usuari,Exemplar
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.db.models import Count
from django.http import JsonResponse
from itertools import chain
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.db.models import Min, Max
from django.db.models.functions import ExtractYear


def perfil(request):
    users = Usuari.objects.all()
    if request.user.is_authenticated and not request.user.autentificacio:
        return redirect('change')
    ciclos = Cicle.objects.all()
    success_message = "hola"
    
    if request.method == "POST":
        user_id = request.POST.get('id')

        if user_id:
            try:
                
                ciclos = Cicle.objects.all()
                usuario = Usuari.objects.get(pk=user_id)  
                usuario.first_name = request.POST['first_name']
                usuario.last_name = request.POST['last_name']
                usuario.telefon = request.POST['telefon']
                usuario.data_naixement = request.POST['data_naixement']
                
                if 'rol' in request.POST and usuario.rol != 'Alumne':
                    usuario.rol = request.POST.get('rol')
                
                if 'email' in request.POST:
                    usuario.email = request.POST['email']
                    
                cicle_id = request.POST.get('cicle')
                if cicle_id:
                    # Buscar la instancia del ciclo en la base de datos
                    cicle = Cicle.objects.get(pk=cicle_id)
                    # Asignar el ciclo al usuario
                    usuario.cicle = cicle
                usuario.save()
                messages.success(request, 'Datos actualizados correctamente')
                
                generarLog(request, 'INFO', f"Datos actualizados correctamente")
                subir_logs_a_bd(request)
                
                return redirect('perfil')
            except Usuari.DoesNotExist:  # Cambio aquí
                messages.error(request, 'El usuario no existe')
                generarLog(request, 'ERROR', f"El usuario no existe")
                subir_logs_a_bd(request)
                return redirect('perfil')
        else:
            messages.error(request, 'Falta el campo ID')
            generarLog(request, 'ERROR', f"Falta el campo ID")
            subir_logs_a_bd(request)

            return redirect('perfil')

    return render(request, 'perfil.html', {'users': users, 'ciclos': ciclos})

def perfil_editable(request, usuario_id):
    if request.user.is_authenticated and not request.user.autentificacio:
        return redirect('change')
    try:
        usuario = Usuari.objects.get(pk=usuario_id)
        ciclos = Cicle.objects.all()
        if request.method == "POST":
            usuario.first_name = request.POST.get('first_name', usuario.first_name)
            usuario.last_name = request.POST.get('last_name', usuario.last_name)
            usuario.email = request.POST.get('email', usuario.email)
            usuario.telefon = request.POST.get('telefon', usuario.telefon)
            usuario.data_naixement = request.POST.get('data_naixement', usuario.data_naixement)
            usuario.rol = request.POST.get('rol', usuario.rol)
            cicle_id = request.POST.get('cicle')
            if cicle_id:
                # Buscar la instancia del ciclo en la base de datos
                cicle = Cicle.objects.get(pk=cicle_id)
                # Asignar el ciclo al usuario
                usuario.cicle = cicle
            usuario.save()
            messages.success(request, 'Perfil actualizado correctamente')
            return redirect('perfil_editable', usuario_id=usuario_id)
    except Usuari.DoesNotExist:
        messages.error(request, 'El usuario seleccionado no existe')
        return redirect('perfil_editable')

    return render(request, 'perfilEditable.html', {'usuario': usuario, 'ciclos': ciclos})

def index(request):
    books = Llibre.objects.all()
    cds =  CD.objects.all()
    dvds = DVD.objects.all()
    brs = BR.objects.all()
    dispositius = Dispositiu.objects.all()

    all_items = list(books) + list(cds) + list(dvds) + list(brs) + list(dispositius)
    if request.user.is_authenticated and not request.user.autentificacio:
        return redirect('change')
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
    min_year = Catalog.objects.aggregate(min_year=ExtractYear(Min('fecha_publicacion')))['min_year']
    max_year = Catalog.objects.aggregate(max_year=ExtractYear(Max('fecha_publicacion')))['max_year']
    query = request.GET.get('searcher')
    has_stock = request.GET.get("has_stock", "off") == "on"
    
    product_type = request.GET.get('product_type')
    start_year = request.GET.get('start_year')
    end_year = request.GET.get('end_year')
    estado = request.GET.get('estado')

    if product_type:
        if product_type == 'llibre':
            items = Llibre.objects.all()
        elif product_type == 'cd':
            items = CD.objects.all()
        elif product_type == 'dvd':
            items = DVD.objects.all()
        elif product_type == 'br':
            items = BR.objects.all()
        elif product_type == 'dispositiu':
            items = Dispositiu.objects.all()
    else:
        items = list(chain(Llibre.objects.all(), CD.objects.all(), DVD.objects.all(), BR.objects.all(), Dispositiu.objects.all()))

    if start_year and end_year:
        start_date = datetime(int(start_year), 1, 1)
        end_date = datetime(int(end_year), 12, 31)
        items = [item for item in items if start_date <= datetime.combine(item.fecha_publicacion, datetime.min.time()) <= end_date]
    
    if query:
        items = [item for item in items if query.lower() in item.nom.lower()]

    # Filtrar por estado si se proporciona
    if estado:
        filtered_items = []
        for item in items:
            if Exemplar.objects.filter(catalogo=item, estat=estado).exists():
                filtered_items.append(item)
        items = filtered_items

    paginator = Paginator(items, 25)
    page_number = request.GET.get('page')
    try:
        items = paginator.page(page_number)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    
    return render(request, 'search_results.html', {
        'items': items,
        'query': query,
        'has_stock': has_stock,
        'product_type': product_type,
        'start_year': start_year,
        'end_year': end_year,
        'fecha_minima': min_year, 
        'fecha_maxima': max_year
    })

# def search_results(request):
#     generarLog(request, 'INFO', f"BUSQUEDA REALIZADA")
#     subir_logs_a_bd(request)
    
#     query = request.GET.get('searcher')
#     has_stock = request.GET.get("has_stock", "off") == "on"
    
#     books = Llibre.objects.filter(Q(nom__icontains=query))
#     cds = CD.objects.filter(Q(nom__icontains=query))
#     dvds = DVD.objects.filter(Q(nom__icontains=query))
#     brs = BR.objects.filter(Q(nom__icontains=query))
#     dispositivos = Dispositiu.objects.filter(Q(nom__icontains=query))
    
#     # Fusionar todas las consultas en una sola lista
#     all_items = list(chain(books, cds, dvds, brs, dispositivos))
    
#     # Paginar la lista combinada
#     paginator = Paginator(all_items, 25)  # Muestra 50 elementos por página
    
#     page_number = request.GET.get('page')
#     try:
#         items = paginator.page(page_number)
#     except PageNotAnInteger:
#         # Si la página no es un número entero, muestra la primera página
#         items = paginator.page(1)
#     except EmptyPage:
#         # Si la página está fuera del rango, muestra la última página de resultados
#         items = paginator.page(paginator.num_pages)
    
#     return render(request, 'search_results.html', {
#         'items': items,
#         'query': query,
#         'has_stock': has_stock,
#     })



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
    if request.user.is_authenticated and not request.user.autentificacio:
        return redirect('change')
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

def Prestecs(request):
    if request.user.is_authenticated and not request.user.autentificacio:
        return redirect('change')
    
    # Obtener todos los usuarios que tienen préstamos
    usuarios_con_prestamo = Usuari.objects.filter(prestec__isnull=False).distinct().order_by('-id')

    # Paginar la lista de usuarios
    paginator = Paginator(usuarios_con_prestamo, 10)  # Show 10 usuarios per page
    page = request.GET.get('page')
    try:
        usuarios = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        usuarios = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        usuarios = paginator.page(paginator.num_pages)

    return render(request, 'Prestecs.html', {'usuarios_con_prestamo': usuarios})



def llistarprestecs(request):
    if request.user.is_authenticated and not request.user.autentificacio:
        return redirect('change')
    if request.method == 'POST':
        # Procesar los datos del formulario de préstamo
        usuario_id = request.POST.get('usuari')
        catalogo_id = request.POST.get('catalog')
        
        # Obtener la fecha actual
        fecha_prestamo = timezone.now().date()
        
        # Calcular la fecha de retorno (un mes después de la fecha de préstamo)
        fecha_retorno = fecha_prestamo + timedelta(days=30)

        # Obtener el usuario y el catálogo
        usuario = Usuari.objects.get(id=usuario_id)
        catalogo = Catalog.objects.get(id=catalogo_id)

        # Verificar si hay suficientes elementos en el catálogo
        if catalogo.cantidad > 0:
            # Crear el préstamo
            prestamo = Prestec.objects.create(usuari=usuario, catalog=catalogo, data_prestec=fecha_prestamo, data_retorn=fecha_retorno)
            
            # Actualizar la cantidad del objeto en el catálogo específico
            if hasattr(catalogo, 'llibre'):
                catalogo.llibre.cantidad -= 1
                catalogo.llibre.save()
            elif hasattr(catalogo, 'cd'):
                catalogo.cd.cantidad -= 1
                catalogo.cd.save()
            elif hasattr(catalogo, 'dvd'):
                catalogo.dvd.cantidad -= 1
                catalogo.dvd.save()
            elif hasattr(catalogo, 'br'):
                catalogo.br.cantidad -= 1
                catalogo.br.save()
            elif hasattr(catalogo, 'dispositiu'):
                catalogo.dispositiu.cantidad -= 1
                catalogo.dispositiu.save()
            
            # Redirigir a alguna página de éxito o a donde desees
            return redirect('Prestecs')
        else:
            # Manejar el caso en el que no haya suficientes elementos en el catálogo
            # Puedes mostrar un mensaje de error o redirigir a alguna página de error
            pass

    # Obtener los usuarios que tienen menos de 3 préstamos
    usuarios_con_prestamo = Usuari.objects.annotate(num_prestamos=Count('prestec')).filter(num_prestamos__lt=3).distinct()
    
    # Obtener los catálogos disponibles con cantidad mayor a 1
    catalog_items = Catalog.objects.annotate(
        available_count=F('cantidad')
    ).filter(
        available_count__gt=0
    )

    # Pasar los usuarios y la fecha actual a la plantilla
    return render(request, 'llistarPrestecs.html', {'usuarios_con_prestamo': usuarios_con_prestamo, 'catalog_items': catalog_items})


def listUsers(request):
    if request.user.is_authenticated and not request.user.autentificacio:
        return redirect('change')
    
    users = Usuari.objects.all()  # Obtiene todos los usuarios
    
    paginator = Paginator(users, 10)  # Crea un paginador con 10 usuarios por página
    page_number = request.GET.get('page')
   
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # Si el número de página no es un entero, muestra la primera página
        page_obj = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango (por ejemplo, 9999), muestra la última página
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'listUsers.html', {'usuarios': page_obj})


def dashboard(request):
    if request.user.is_authenticated and not request.user.autentificacio:
        return redirect('change')
    return render(request, 'dashboard.html')

@login_required
@check_user_able_to_see_page("Bibliotecari", "Admin")
def register(request):
    if request.user.is_authenticated and not request.user.autentificacio:
        return redirect('change')
    centredata = Centre.objects.all()
    roles_data = Usuari.ROLES_CHOICES
    cicledata = Cicle.objects.all()
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        id_centre = request.POST.get('id_centre')
        id_cicle = request.POST.get('id_cicle')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        birthdate = request.POST.get('birthdate')
        rol = request.POST.get('roles')
        telefon = request.POST.get('telefon')
        if password1 != password2:
            return render(request, 'user_creation.html', {'centredata': centredata, 'cicledata': cicledata, 'error_message': 'Las contraseñas no coinciden'})

        centre_instance = Centre.objects.get(pk=id_centre)
        cicle_instance = Cicle.objects.get(pk=id_cicle)

        user = Usuari.objects.create_user(username=email, email=email, password=password1, first_name=first_name, last_name=last_name, centre_id=id_centre, cicle=cicle_instance, telefon = telefon,data_naixement = birthdate, rol = rol )
        user.save()

        return redirect('index')

    return render(request, 'user_creation.html', {'centredata': centredata, 'cicledata': cicledata, 'roles_data': roles_data})

class ChangePass(PasswordChangeView):
    template_name = "registration/change_pass.html"
    success_url = reverse_lazy("logout")
    def form_valid(self, form):
        if not self.request.user.autentificacio:
            self.request.user.autentificacio = True
            self.request.user.save()
        return super().form_valid(form)

class ChangePassDone(PasswordChangeDoneView):
    template_name = "registration/change_pass_done.html"



class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'registration/reset_pass.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('index')

def ResetPassDone(request):
    return render (request, "registration/reset_pass_done.html")



def buscar_autocompletado(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        has_stock = request.GET.get('has_stock', '')

        items = []

        if query:
            # Realizar la búsqueda en la base de datos
            libros = Llibre.objects.filter(nom__icontains=query)
            cds = CD.objects.filter(nom__icontains=query)
            dvds = DVD.objects.filter(nom__icontains=query)
            brs = BR.objects.filter(nom__icontains=query)
            dispositius = Dispositiu.objects.filter(nom__icontains=query)

            # Combinar todos los resultados en una lista
            items = list(libros) + list(cds) + list(dvds) + list(brs) + list(dispositius)

            # Aplicar filtro de stock si es necesario
            if has_stock == 'true':
                items = [item for item in items if item.cantidad > 0]

            items = items[:5]  # Limitar los resultados a los primeros 5

        # Convertir los resultados en un formato JSON
        data = [{'nombre': obj.nom, 'tipo_material': type(obj).__name__} for obj in items]

        # Devolver los resultados como respuesta JSON
        return JsonResponse(data, safe=False)

    return JsonResponse([], safe=False)
