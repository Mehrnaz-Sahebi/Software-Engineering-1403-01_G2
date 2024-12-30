from django.urls import path

import registration.views as registration

from . import views

app_name = "group10"
urlpatterns = [
    path("/nextword", views.home, name="home"),
    path("/nextword/suggest", views.home, name="suggest"),
    path("/nextword/signup/", registration.SignupPage, name="signup"),
    path("/nextword/login/", registration.LoginPage, name="login"),
    path("/nextword/logout/", registration.LogoutPage, name="logout"),
]
