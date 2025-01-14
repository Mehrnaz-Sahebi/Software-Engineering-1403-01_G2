from django.urls import path
from . import views
app_name = 'group8'  
urlpatterns = [
    path('', views.home, name='group8'),
    path('home/', views.home, name='group8'),
    path('login/', views.login, name='login'),
    path('submit-text/', views.submit_text, name='submit_text'),
]