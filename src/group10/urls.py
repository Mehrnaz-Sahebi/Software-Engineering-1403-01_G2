from django.urls import path
from . import views

app_name = "group10"
urlpatterns = [
    path("next-word/home/", views.home, name="home"),
    path("next-word/suggest/", views.suggest, name="suggest"),
    path("next-word/signup/", views.SignupPage, name="signup"),
    path("next-word/login/", views.LoginPage, name="login"),
    path("next-word/logout/", views.LogoutPage, name="logout"),
]
