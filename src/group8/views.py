import json
import os
import logging
import datetime
import base64
import pickle
from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .rabbitmq_client import RabbitMQClient 
import mysql.connector as mysql
from mysql.connector import Error
from django.conf import settings
from django.db import connection
import threading
import queue
 

from database.query import get_user_id_by_username, get_posts_for_user 


rabbitmq_client = RabbitMQClient()


def get_db_connection(): 
    DB_HOST = 'localhost'
    DB_PORT = 3306
    DB_USER = 'root' 
    DB_PASSWORD = 'password'
    DB_NAME = 'mydatabase'
     
    return mysql.connect( 
        host=DB_HOST, 
        port=DB_PORT, 
        user=DB_USER, 
        password=DB_PASSWORD, 
        database=DB_NAME 
    ) 
    
    
def get_mysql_connection():
    DB_NAME = 'defaultdb'
    DB_USER = 'avnadmin'
    DB_PASSWORD = 'AVNS_QXs1v9qBTveDtLIXZfW'
    DB_HOST = 'mysql-374f4726-majidnamiiiii-e945.a.aivencloud.com'
    DB_PORT = 11741  # or as int
    
    try:
        logging.basicConfig(level=logging.DEBUG)
        connection = mysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            ssl_disabled=True,  # Disable SSL temporarily
            connect_timeout=10
        )
        return connection
    except Error as e:
        print("Error connecting to MySQL: ", e)
        return None
        

from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.utils.timezone import now

def get_user_id_from_session(session_key):
    try:

        session = Session.objects.get(session_key=session_key, expire_date__gte=now())
        session_data = session.get_decoded()
    
        user_id = session_data.get('_auth_user_id')
        if user_id:
            #user = User.objects.get(id=user_id)
            return user_id
        return None
    except Session.DoesNotExist:
        return None
    except User.DoesNotExist:
        return None


@csrf_exempt
def submit_text_in_history(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)
        text = data.get('text')
        if not text:
            return JsonResponse({"error": "No text provided"}, status=400)
    except Exception as e:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)


    session_key = request.COOKIES.get('sessionid')
    if not session_key:
        return JsonResponse({"error": "No sessionid cookie found"}, status=401)


    user_id = get_user_id_from_session(session_key)
    if not user_id:
        return JsonResponse({"error": "Invalid or expired session"}, status=401)

    conn = get_mysql_connection()
    
    
    
    if not conn:
        return JsonResponse({"error": "Could not connect to MySQL"}, status=500)

    try:
        cursor = conn.cursor()


        # create_table_query = """
        #    CREATE TABLE IF NOT EXISTS text_history (
        #        id INT AUTO_INCREMENT PRIMARY KEY,
        #        user_id INT NOT NULL,
        #        file_name VARCHAR(255) NOT NULL,
        #        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        #    )
        #"""
        #cursor.execute(create_table_query)
        #conn.commit()


        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        file_name = f"text_{user_id}_{timestamp}.txt"
        uploads_dir = os.path.join(settings.BASE_DIR, 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        full_file_path = os.path.join(uploads_dir, file_name)
        with open(full_file_path, 'w', encoding='utf-8') as f:
            f.write(text)


        insert_query = """
            INSERT INTO text_history (user_id, file_name)
            VALUES (%s, %s)
        """
        cursor.execute(insert_query, (user_id, file_name))
        conn.commit()

        return JsonResponse({
            "message": "Text submitted and file saved successfully",
            "file_name": file_name
        }, status=200)

    except Exception as e:
        print("Error in submit_text_in_history:", e)
        return JsonResponse({"error": "Database error"}, status=500)
    finally:
        cursor.close()
        conn.close()


@csrf_exempt
def get_submit_texts(request):
    if request.method != 'GET':
        return JsonResponse({"error": "Invalid request method"}, status=405)


    session_key = request.COOKIES.get('sessionid')
    if not session_key:
        return JsonResponse({"error": "No sessionid cookie found"}, status=401)


    user_id = get_user_id_from_session(session_key)
    if not user_id:
        return JsonResponse({"error": "Invalid or expired session"}, status=401)


    conn = get_mysql_connection()
    if not conn:
        return JsonResponse({"error": "Could not connect to MySQL"}, status=500)

    try:
        cursor = conn.cursor(dictionary=True)


        #create_table_query = """
        #    CREATE TABLE IF NOT EXISTS text_history (
        #        id INT AUTO_INCREMENT PRIMARY KEY,
        #        user_id INT NOT NULL,
        #        file_name VARCHAR(255) NOT NULL,
        #        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        #    )
        #"""
        #cursor.execute(create_table_query)
        #conn.commit()


        select_query = """
            SELECT id, file_name, created_at
            FROM text_history
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT 10
        """
        cursor.execute(select_query, (user_id,))
        rows = cursor.fetchall()

        return JsonResponse({
            "submissions": rows
        }, status=200, safe=False)

    except Exception as e:
        print("Error in get_submit_texts:", e)
        return JsonResponse({"error": "Database error"}, status=500)
    finally:
        cursor.close()
        conn.close()

 
 
@csrf_exempt 
def submit_text(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text')
        

        response_queue = queue.Queue()
        
        def on_response(response):
            print(response)
            if isinstance(response, list) and len(response) > 0:
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


        rabbitmq_client.send_message(
            json.dumps({"text": text}, ensure_ascii=False),
            on_response
        )

        try:
            final_response = response_queue.get(timeout=30)  # Wait up to 30 seconds
        except queue.Empty:
            return JsonResponse({"error": "Timeout waiting for response"}, status=504)


        return JsonResponse(final_response, status=200)


    return JsonResponse({"error": "Invalid request method"}, status=405)

        
        
'''        
def home(request):
    return render (request , 'group8.html' , {'group_number': '8'})
    '''
    

def home(request):
    redirect_url = f"http://localhost:5173/"
    return redirect(redirect_url)
        
'''        
def home(request):
    session_id = request.COOKIES.get('csrftoken')
    if session_id:
        redirect_url = f"http://localhost:5173/"
        return redirect(redirect_url)
    else:
        return render(request, 'group8.html', {'group_number': '8'})
'''





def get_last_5_text_files_content(request):
    if request.method != 'GET':
        return JsonResponse({"error": "Invalid request method"}, status=405)

    """
    Get the content of the last 5 created text files in the specified directory
    that start with "text_{user_id}_" based on the user ID extracted from the request.

    Args:
        request (HttpRequest): The HTTP request containing user session or data.

    Returns:
        JsonResponse: A JSON response containing file names as keys and their content as values.
    """
    try:
        session_key = request.COOKIES.get('sessionid')
        if not session_key:
            return JsonResponse({"error": "No sessionid cookie found"}, status=401)

        user_id = get_user_id_from_session(session_key)
        if not user_id:
            return JsonResponse({"error": "Invalid or expired session"}, status=401)

        directory = os.path.join(settings.BASE_DIR, 'uploads')


        files = [
            os.path.join(directory, f) for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f))
            and f.startswith(f"text_{user_id}_")
            and f.endswith('.txt')
        ]


        files.sort(key=os.path.getctime, reverse=True)


        last_5_files = files[:5]


        file_contents = {}
        for file in last_5_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                file_contents[os.path.basename(file)] = content


        return JsonResponse(
            file_contents,
            safe=False,
            json_dumps_params={'ensure_ascii': False, 'indent': 4}
        )

    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=500,
            json_dumps_params={'ensure_ascii': False, 'indent': 4}
        )

