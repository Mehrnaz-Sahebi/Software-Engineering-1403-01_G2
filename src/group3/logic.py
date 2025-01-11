from django.shortcuts import render
from hazm import Normalizer
from .models import TextOptimization

def process_input(input_text):
    normalizer = Normalizer()
    optimized_text = normalizer.normalize(input_text)
    return optimized_text
    