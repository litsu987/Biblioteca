from django import forms
from .models import Usuari
from django.contrib.auth.forms import UserCreationForm
 
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone_no = forms.CharField(max_length = 20)
    first_name = forms.CharField(max_length = 20)
    last_name = forms.CharField(max_length = 20)
    class Meta:
        model = Usuari
        fields = ['first_name','last_name', 'email', 'phone_no', 'password1', 'password2']
