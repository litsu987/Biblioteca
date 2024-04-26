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
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from .decorators import check_user_able_to_see_page
from .forms import UsuariRegistroForm


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
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            generarLog(request, 'INFO', f"lOGIN CORRECTO.")
            subir_logs_a_bd(request)
            return redirect('dashboard')  
        else:
            messages.error(request, "Correo electrónico o contraseña inválidos.")
            generarLog(request, 'ERROR', f"El correo electrónico o contraseña invalidos.")
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
    messages.success(request, 'Torna aviat!!')
    generarLog(request, 'INFO', f"LOGOUT.")
    subir_logs_a_bd(request)
    return redirect('index')

@login_required
@check_user_able_to_see_page("Bibliotecari", "Admin")
def library_loan(request):
    if request.method == 'POST':
        form = UsuariRegistroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')  # Cambiar 'ruta_de_redireccion' por la URL a la que quieras redirigir después del registro exitoso
    else:
        form = UsuariRegistroForm()
    return render(request, 'library_loan.html', {'form': form})


class ChangePass(PasswordChangeView):
    template_name = "registration/resetpass.html"
    success_url = reverse_lazy("reset_done")

class ChangePassDone(PasswordChangeDoneView):
    template_name = "registration/resetpassdone.html"



