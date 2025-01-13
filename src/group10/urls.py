from django.urls import path

from . import views

app_name = "group10"
urlpatterns = [
    path("", views.HomePage, name="home"),
    path("suggest/", views.Suggest, name="suggest"),
    path("signup/", views.SignupPage, name="signup"),
    path("login/", views.LoginPage, name="login"),
    path("logout/", views.LogoutPage, name="logout"),
]
