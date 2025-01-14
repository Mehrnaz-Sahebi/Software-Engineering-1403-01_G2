import json 
from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from .rabbitmq_client import RabbitMQClient 
import mysql.connector as mysql
import threading
import queue
 
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
        
        # A thread-safe FIFO queue to hold the response from the callback
        response_queue = queue.Queue()
        
        def on_response(response):
            """
            This function will be called by your RabbitMQ client once
            the message has been received and processed from the queue.
            """
            # Because the "response" we get back (based on your logs) 
            # looks like a list containing one dict, we can extract 
            # 'results' if that’s the main data needed.
            print(response)
            if isinstance(response, list) and len(response) > 0:
                # The structure of your logged response is:
                # [
                #   {
                #       "correlation_id": "...",
                #       "results": [...]
                #   }
                # ]
                # So to get the "results", you'd do:
                first_item = response[0]
                results = first_item.get("results")
                
                print(results)
                
                response_queue.put({
                    "correlation_id": first_item.get("correlation_id"),
                    "results": results
                })
            else:
                # If there's an error or different format
                response_queue.put({"error": "Invalid response format", "raw": response})

        # Send the text to RabbitMQ for processing
        rabbitmq_client.send_message(
            json.dumps({"text": text}, ensure_ascii=False),
            on_response
        )

        # ----
        # Now we WAIT (block) until we get the result from the queue or timeout.
        # ----
        try:
            final_response = response_queue.get(timeout=30)  # Wait up to 30 seconds
        except queue.Empty:
            return JsonResponse({"error": "Timeout waiting for response"}, status=504)

        # If we got a valid response, send it to the user
        return JsonResponse(final_response, status=200)

    # For methods other than POST
    return JsonResponse({"error": "Invalid request method"}, status=405)

        
        
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
