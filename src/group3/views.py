from django.shortcuts import render
from hazm import Normalizer
from .models import TextOptimization
from .logic import process_input
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

def home(request):
    return render (request , 'group3.html' , {'group_number': '3'})



def optimize_text(request):
    if request.method == 'POST':
        input_text = request.POST.get('text')
        optimized_text = process_input(input_text)
        return render(request, 'group3/result.html', {'optimized_text': optimized_text})

    return render(request, 'group3/optimize.html')


