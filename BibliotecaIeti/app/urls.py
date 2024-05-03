from django.urls import path
from . import views
from .views import ChangePass, ChangePassDone, ResetPasswordView, ResetPassDone

urlpatterns = [
    path("", views.index, name="index"),
    path("dash/", views.dashboard, name="dashboard"),
    path("search/", views.search_results, name="search_results"),
    path("logout/", views.logout_user, name="logout"),  
    path("register/", views.register, name="register"),  
    path("change/", ChangePass.as_view(), name="change"),
    path("reset/", ResetPasswordView.as_view(), name="reset"),  
    path("reset/done/", views.ResetPassDone, name="reset_done"),  
    path("change/done/", ChangePassDone.as_view(), name="change_done"),  
    path('perfil/', views.perfil, name='perfil'),
    path('perfilEditable/<int:usuario_id>', views.perfil_editable, name='perfil_editable'),
    path('importar/', views.importar_Users, name='importar_Users'),
    path('Prestecs/', views.Prestecs, name='Prestecs'),
    path('llistarprestecs/', views.llistarprestecs, name='llistarPrestecs'),
    path('buscar/', views.buscar_autocompletado, name='buscar_autocompletado'),
    
]