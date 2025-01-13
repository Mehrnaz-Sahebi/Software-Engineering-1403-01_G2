import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from django.shortcuts import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from database.query import create_db_connection, save_user
from database.secret import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

# Create your views here.

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def learn_api(request):
    data = json.loads(request.body)
    tokens = data.get("tokens")
    username = data.get("username")

    if not tokens or not isinstance(tokens, list):
        return HttpResponse("Invalid tokens input.", status=400)

    if not username:
        return HttpResponse("Username is required.", status=400)

    mydb = create_db_connection(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
    cursor = mydb.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS G10_word_probabilities_user_customize (
                id INT AUTO_INCREMENT PRIMARY KEY,
                past_word TEXT,
                current_word TEXT,
                count INT DEFAULT 0
            );
        """)

        for i in range(len(tokens) - 1):
            past_word = tokens[i]
            current_word = tokens[i + 1]

            cursor.execute("""
                SELECT count FROM G10_word_probabilities_user_customize
                WHERE past_word = %s AND current_word = %s;
            """, (past_word, current_word))

            result = cursor.fetchone()

            if result:
                new_count = result[0] + 1
                cursor.execute("""
                    UPDATE G10_word_probabilities_user_customize
                    SET count = %s
                    WHERE past_word = %s AND current_word = %s;
                """, (new_count, past_word, current_word))
            else:
                cursor.execute("""
                    INSERT INTO G10_word_probabilities_user_customize (past_word, current_word, count)
                    VALUES (%s, %s, 1);
                """, (past_word, current_word))

        mydb.commit()
    except Exception as e:
        return HttpResponse(f"Error learning data: {str(e)}", status=500)
    finally:
        cursor.close()
        mydb.close()

    return HttpResponse("Learning data successfully updated.", status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def suggest_api(request):
    past_word = request.GET.get("past_word")
    suggestions = []

    if past_word:
        mydb = create_db_connection(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
        cursor = mydb.cursor()

        try:
            cursor.execute(
                """
                SELECT current_word, probability
                FROM G10_word_probabilities
                WHERE past_word = %s
                ORDER BY probability DESC
                LIMIT 5;
                """,
                (past_word,),
            )
            suggestions = cursor.fetchall()
        except Exception:
            return HttpResponse("Error fetching suggestions.", status=500)
        finally:
            cursor.close()
            mydb.close()

    suggestions_data = [
        {"current_word": word, "probability": prob} for word, prob in suggestions
    ]

    return Response({"suggestions": suggestions_data})


@api_view(["GET"])
def csrf_api(request):
    csrf_token = get_token(request)
    return Response({"csrf": csrf_token})


@api_view(["POST"])
def signup_api(request):
    data = json.loads(request.body)

    uname = data.get("username")
    email = data.get("email")
    pass1 = data.get("password1")
    pass2 = data.get("password2")
    name = data.get("name")
    age = data.get("age")

    if pass1 != pass2:
        return HttpResponse("Passwords do not match", status=400)
    else:
        if User.objects.filter(username=uname).exists():
            return HttpResponse("Duplicate username.", status=400)

        try:
            mydb = create_db_connection(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)

            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            save_user(mydb, name, uname, pass1, email, age)
        except Exception:
            return HttpResponse("Registeration failed.", status=403)
        finally:
            mydb.close()

    return HttpResponse()


@api_view(["POST"])
def login_api(request):
    data = json.loads(request.body)

    username = data.get("username")
    pass1 = data.get("pass")

    user = authenticate(request, username=username, password=pass1)

    if user is None:
        return HttpResponse("Username or Password is incorrect.", status=403)

    login(request, user)

    return HttpResponse()


@api_view(["GET"])
def logout_api(request):
    logout(request)

    return HttpResponse()
