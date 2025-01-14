from django.urls import path
from . import views

app_name = "group9"
urlpatterns = [
    path("", views.home, name="group9"),
    path("signup/", views.SignupPage, name="signup"),
    path("login/", views.LoginPage, name="login"),
    path("logout/", views.LogoutPage, name="logout"),
    path("optimize/", views.OptimizePage, name="optimize"),
    path("history/", views.HistoryPage, name="history"),
]
