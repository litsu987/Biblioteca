from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dash/", views.dashboard, name="dashboard"),
    path("search/", views.search_results, name="search_results"),
    path('logout/', views.logout_user, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfilEditable/', views.perfil_editable, name='perfil_editable'),
    ]
