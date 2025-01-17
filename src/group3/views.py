from django.shortcuts import render
from .models import TextOptimization
from .logic import process_input
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .database import query,secret
from .parse import find_suggestions
from .logic import process_input
from .serializer import SuggestionSerializer, TextSuggestionSerializer
from .database.query import save_suggestion
# Create your views here.
mydb = query.create_db_connection(secret.DB_HOST, secret.DB_PORT, secret.DB_USER, secret.DB_PASSWORD, secret.DB_NAME)
def home(request):
    return render (request , 'group3.html' , {'group_number': '3'})



class TextMistakesAPIView(APIView):
    def post(self, request):
        input_text = request.data.get('text', '')
        if not input_text:
            return Response({"error": "No text provided"}, status=status.HTTP_400_BAD_REQUEST)

        mistakes = process_text(input_text)
        optimized_text = find_output(input_text)
        try:
            text_optimization = TextOptimization.objects.create(
                    input_text=input_text,
                    optimized_text=optimized_text
                    )
        except Exception as e:
            print(str(e))
        try:
            for suggestion in mistakes:
                suggestion_serializer = SuggestionSerializer(data=suggestion)
                if suggestion_serializer.is_valid():
                    start = suggestion_serializer.validated_data['start']
                    end = suggestion_serializer.validated_data['end']
                    suggestion_text = suggestion_serializer.validated_data['suggest']
                    save_suggestion(mydb, start, end, suggestion_text)
                else:
                    print("Validation errors:", suggestion_serializer.errors)
                    return Response({"error": suggestion_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"{e} my error")
        
        return Response({"suggestions": mistakes}, status=status.HTTP_200_OK)


def find_output(text):
    return process_input(text)


def process_text(text):
    output_text = process_input(text)
    suggestions = find_suggestions(text, output_text)
    return suggestions


    


