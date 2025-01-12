from django.urls import path
from . import views

app_name = 'group9'
urlpatterns = [
  path('', views.home, name='group9'),
  path('signup/', views.signup_page, name='signup'),
  path('login/', views.login_page, name='login'),
  path('logout/', views.logout_page, name='logout'),
  path('<path:path>', views.dynamic_view, name='dynamic_view'),

] 