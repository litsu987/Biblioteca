from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuari

class UsuariRegistroForm(UserCreationForm):
    class Meta:
        model = Usuari
        fields = ['email', 'password1', 'password2', 'data_naixement', 'centre', 'cicle', 'imatge', 'first_name', 'last_name', 'telefon', 'rol']
