from django.urls import path
from django.views.static import serve

from FarsiAid_website.settings import STATICFILES_DIRS

from . import views

app_name = "group10"
urlpatterns = [
    path("api/suggest/", views.suggest_api, name="suggest"),
    path("api/learn/", views.learn_api, name="learn"),
    path("api/csrf/", views.csrf_api, name="csrf"),
    path("api/signup/", views.signup_api, name="signup"),
    path("api/login/", views.login_api, name="login"),
    path("api/logout/", views.logout_api, name="logout"),
    path("<path:path>", serve, {"document_root": STATICFILES_DIRS[0]}),
]
