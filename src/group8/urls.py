from django.urls import path
from . import views

app_name = 'group8'

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='group8'),
    path('submit-text/', views.submit_text, name='submit_text'),
    path('submit-text-in-history/', views.submit_text_in_history, name='submit_text_in_history'),
    path('get-submit-texts/', views.get_submit_texts, name='get_submit_texts'),
]

