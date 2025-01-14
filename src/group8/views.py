import json
import time
from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.models import User
from .rabbitmq_client import RabbitMQClient 
import mysql.connector as mysql 
 
# Database connection setup (for Django, make sure to use the provided connection function) 
from database.query import get_user_id_by_username, get_posts_for_user 


rabbitmq_client = RabbitMQClient()

# Function to create a database connection 
def get_db_connection(): 
    DB_HOST = 'localhost'  # Or your DB host 
    DB_PORT = 3306  # Default MySQL port 
    DB_USER = 'root'  # Replace with your DB user 
    DB_PASSWORD = 'password'  # Replace with your DB password 
    DB_NAME = 'mydatabase'  # Replace with your DB name 
     
    return mysql.connect( 
        host=DB_HOST, 
        port=DB_PORT, 
        user=DB_USER, 
        password=DB_PASSWORD, 
        database=DB_NAME 
    ) 
 
# Login view to authenticate the user 
@csrf_exempt 
def login(request): 
    if request.method == 'POST': 
        data = json.loads(request.body) 
        #username = data.get('username') 
        #password = data.get('password') 
         
        # Create a DB connection 
        #db_connection = get_db_connection() 
         
        # Get the user ID from the database using the username 
        #user_id = get_user_id_by_username(db_connection, username) 
         
        #if user_id: 
            # Here we assume that password is correctly matched 
            # You can modify this part to validate the password if needed 
        #    return JsonResponse({"message": "Login successful", "user_id": user_id}, status=200) 
        #else: 
            #return JsonResponse({"message": "Invalid credentials"}, status=401) 
    if request.method == 'GET': 
        return JsonResponse({"message": "Login page"}, status=200) 
 
# Submit text view to handle user text submissions 
@csrf_exempt 
def submit_text(request): 
    if request.method == 'POST': 
        data = json.loads(request.body) 
        text = data.get('text')

        # Ensure the response data is globally accessible
        response_data = None

        def on_response(response): 
            nonlocal response_data  # Use nonlocal to modify the outer variable
            response_data = response

        # Send the text to RabbitMQ for processing
        rabbitmq_client.send_message(json.dumps({"text": text}, ensure_ascii=False), on_response)

        # Wait for the Go server's response before returning it
        timeout = 10  # seconds
        elapsed = 0
        while response_data is None and elapsed < timeout:
            time.sleep(0.1)
            elapsed += 0.1

        if response_data is not None:
            # Return the JSON response from the Go server
            return JsonResponse(response_data, safe=False, status=200)
        else:
            # Handle timeout or missing response
            return JsonResponse({"error": "No response from Go server within the timeout period"}, status=504)

    return JsonResponse({"error": "Invalid request method"}, status=405)
        
        
'''        
def home(request):
    return render (request , 'group8.html' , {'group_number': '8'})
    '''
    

def home(request):
    session_id = request.COOKIES.get('csrftoken')
    print(settings.SESSION_COOKIE_NAME)
    session_cookie_name = settings.SESSION_COOKIE_NAME
    session_id = request.COOKIES.get(session_cookie_name)
    print(session_id)
    if session_id:
        redirect_url = f"http://localhost:5173/loggedIn?sessionId={session_id}"
        return redirect(redirect_url)
    else:
        return render(request, 'group8.html', {'group_number': '8'})
        
@csrf_exempt 
def submit_text(request): 
    if request.method == 'POST': 
        data = json.loads(request.body) 
        text = data.get('text')

        # Ensure the response data is globally accessible
        response_data = None

        def on_response(response): 
            nonlocal response_data  # Use nonlocal to modify the outer variable
            response_data = response

        # Send the text to RabbitMQ for processing
        rabbitmq_client.send_message(json.dumps({"text": text}, ensure_ascii=False), on_response)

        # Wait for the Go server's response before returning it
        timeout = 10  # seconds
        elapsed = 0
        while response_data is None and elapsed < timeout:
            time.sleep(0.1)
            elapsed += 0.1

        if response_data is not None:
            # Return the JSON response from the Go server
            return JsonResponse(response_data, safe=False, status=200)
        else:
            # Handle timeout or missing response
            return JsonResponse({"error": "No response from Go server within the timeout period"}, status=504)

    return JsonResponse({"error": "Invalid request method"}, status=405)
