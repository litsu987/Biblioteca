from django.urls import path
from . import views
from .views import ChangePass, ChangePassDone

urlpatterns = [
    path("", views.index, name="index"),
    path("dash/", views.dashboard, name="dashboard"),
    path("search/", views.search_results, name="search_results"),
    path("logout/", views.logout_user, name="logout"),  
    path("loan/", views.library_loan, name="loan"),  
    path("reset/", ChangePass.as_view(), name="reset"),  
    path("reset/done/", ChangePassDone.as_view(), name="reset_done"),  
]
