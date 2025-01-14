import json 
from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
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
    if request.method == 'GET': 
        session_id = request.COOKIES.get('csrftoken')
        #if not session_id:
        #    return JsonResponse({"error": "User not authenticated"}, status=401)
        data = json.loads(request.body) 
        #user_id = data.get('user_id') 
        text = data.get('text') 
        if not text:
            return JsonResponse({"error": "Text is required"}, status=400)
        # db_connection = get_db_connection() 
         
        # Get posts for user (could also use the search function if needed) 
        # posts = get_posts_for_user(db_connection, user_id) 
         
        # Send the post text to the Go server via RabbitMQ  
        #user_text = UserText(user_id=session_id, text=text)
        #user_text.save()
        rabbitmq_response = {}

            # Callback function to handle RabbitMQ response
        def on_response(response):
            nonlocal rabbitmq_response
            rabbitmq_response = json.loads(response)
 
        # Send text and posts to RabbitMQ for processing 
        #rabbitmq_client.send_message(json.dumps({"text": text, "posts": posts, "user_id": user_id}), on_response) 
        rabbitmq_client.send_message(
                json.dumps({"text": text}, ensure_ascii=False),
                on_response=on_response
            )
        if not rabbitmq_response:
                return JsonResponse({"message": "Processing delayed, no response from RabbitMQ yet"}, status=202)

        return JsonResponse({"rabbitmq_response": rabbitmq_response}, status=200)

        
        
'''        
def home(request):
    return render (request , 'group8.html' , {'group_number': '8'})
    '''
    

def home(request):
    session_id = request.COOKIES.get('csrftoken')
    if session_id:
        redirect_url = f"http://localhost:5173/loggedIn?sessionId={session_id}"
        return redirect(redirect_url)
    else:
        return render(request, 'group8.html', {'group_number': '8'})
