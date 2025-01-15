from django.urls import path
from . import views

app_name = 'group8'

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='group8'),
    path('submit-text/', views.submit_text, name='submit_text'),
    path('submit_text_in_history/', views.submit_text_in_history, name='submit_text_in_history'),
    path('get_submit_texts/', views.get_submit_texts, name='get_submit_texts'),
    path('get_last_5_text_files_content/', views.get_last_5_text_files_content, name='get_last_5_text_files_content'),
]

