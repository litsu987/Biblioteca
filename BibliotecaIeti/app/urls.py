from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dash/", views.dashboard, name="dashboard"),
    path("search/", views.search_results, name="search_results"),
    path('logout/', views.logout_user, name='logout'),
    path('importar/', views.importar_Users, name='importar_Users.html'),
    ]
