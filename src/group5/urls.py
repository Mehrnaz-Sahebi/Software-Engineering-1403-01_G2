from django.urls import path

from . import views

app_name = 'group5'
urlpatterns = [
    path('home/', views.home, name='group5'),
    path('suggest/', views.suggest_word_api, name='suggest-word'),
    path('add/', views.add_ngram_api, name='add-ngram'),
]
