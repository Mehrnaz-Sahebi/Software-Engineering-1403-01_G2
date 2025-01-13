from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from database.query import create_db_connection, save_user
from database.secret import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

# Create your views here.

GLOBAL_DB_CONNECTION = create_db_connection(
    DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def suggest_api(request):
    past_word = request.GET.get("past_word")
    suggestions = []

    if past_word:
        cursor = GLOBAL_DB_CONNECTION.cursor()

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

    suggestions_data = [
        {"current_word": word, "probability": prob} for word, prob in suggestions
    ]

    return JsonResponse({"suggestions": suggestions_data})


@api_view(["GET"])
def csrf_api(request):
    csrf_token = get_token(request)
    return JsonResponse({"csrf": csrf_token})


@api_view(["POST"])
def signup_api(request):
    uname = request.data.get("username")
    email = request.data.get("email")
    pass1 = request.data.get("password1")
    pass2 = request.data.get("password2")
    name = request.data.get("name")
    age = request.data.get("age")

    if not all([uname, email, pass1, pass2, name, age]):
        return JsonResponse({"error": "All fields are required."}, status=400)

    if pass1 != pass2:
        return JsonResponse({"error": "Passwords do not match."}, status=400)

    if User.objects.filter(username=uname).exists():
        return JsonResponse({"error": "Username already exists."}, status=400)

    try:
        save_user(GLOBAL_DB_CONNECTION, name, uname, pass1, email, age)

        my_user = User.objects.create_user(username=uname, email=email, password=pass1)
        my_user.save()

    except Exception as e:
        return JsonResponse(
            {"error": "Registration failed.", "details": str(e)},
            status=403,
        )

    return JsonResponse({"message": "Registered successfully."}, status=201)


@api_view(["POST"])
def login_api(request):
    if request.content_type != "application/json":
        return JsonResponse(
            {"error": "Invalid content type. Expected application/json."}, status=400
        )

    username = request.data.get("username")
    pass1 = request.data.get("pass")

    if not all([username, pass1]):
        return JsonResponse({"error": "All fields are required."}, status=400)

    user = authenticate(request, username=username, password=pass1)
    if user is None:
        return JsonResponse({"error": "Username or password is incorrect."}, status=403)

    login(request, user)

    return JsonResponse({"message": "Logged in successfully."}, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logout_api(request):
    logout(request)
    return JsonResponse({"message": "Logged out successfully."}, status=200)
