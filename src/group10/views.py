import threading
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from database.query import create_db_connection, save_user
from database.secret import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

# Create your views here.

connection_lock = threading.Lock()

GLOBAL_DB_CONNECTION = None


def get_global_db_connection():
    global GLOBAL_DB_CONNECTION

    with connection_lock:
        if GLOBAL_DB_CONNECTION is None:
            try:
                GLOBAL_DB_CONNECTION = create_db_connection(
                    DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
                )
            except Exception as e:
                print(f"Failed to reconnect to the database: {e}")
                raise

    return GLOBAL_DB_CONNECTION


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def learn_api(request):
    if request.content_type != "application/json":
        return JsonResponse(
            {"error": "invalid content type. expected application/json."}, status=400
        )

    username = request.data.get("username")
    tokens = request.data.get("tokens")

    if not username:
        return JsonResponse({"error": "username is required."}, status=400)

    if not tokens or not isinstance(tokens, list):
        return JsonResponse({"error": "invalid tokens."}, status=400)

    cursor = get_global_db_connection().cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS G10_word_probabilities_user_customize (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username TEXT,
                past_word TEXT,
                current_word TEXT,
                count INT DEFAULT 0
            );
        """)

        for i in range(len(tokens) - 1):
            past_word = tokens[i]
            current_word = tokens[i + 1]

            cursor.execute(
                """
                SELECT count FROM G10_word_probabilities_user_customize
                WHERE username = %s AND past_word = %s AND current_word = %s;
            """,
                (username, past_word, current_word),
            )

            result = cursor.fetchone()

            if result:
                new_count = result[0] + 1
                cursor.execute(
                    """
                    UPDATE G10_word_probabilities_user_customize
                    SET count = %s
                    WHERE username = %s AND past_word = %s AND current_word = %s;
                """,
                    (new_count, username, past_word, current_word),
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO G10_word_probabilities_user_customize (username, past_word, current_word, count)
                    VALUES (%s, %s, %s, 1);
                """,
                    (username, past_word, current_word),
                )

        get_global_db_connection().commit()

    except Exception as e:
        return JsonResponse(
            {"error": "learning failed.", "details": str(e)},
            status=500,
        )
    finally:
        if cursor:
            cursor.close()

    return JsonResponse({"message": "learn data updated successfully."}, status=200)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def suggest_api(request):
    if request.content_type != "application/json":
        return JsonResponse(
            {"error": "invalid content type. expected application/json."}, status=400
        )

    username = request.data.get("username")
    past_word = request.data.get("past_word")

    if not username:
        return JsonResponse({"error": "username is required."}, status=400)

    if not past_word:
        return JsonResponse({"error": "past_word is required."}, status=400)

    suggestions = []

    cursor = get_global_db_connection().cursor()

    try:
        cursor.execute(
            """
            SELECT current_word
            FROM G10_word_probabilities_improve_parsivar
            WHERE past_word = %s
            ORDER BY probability DESC
            LIMIT 3;
            """,
            (past_word,),
        )

        global_suggestions = [row[0] for row in cursor.fetchall()]

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS G10_word_probabilities_user_customize (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username TEXT,
                past_word TEXT,
                current_word TEXT,
                count INT DEFAULT 0
            );
        """)

        cursor.execute(
            """
            SELECT current_word
            FROM G10_word_probabilities_user_customize
            WHERE username = %s AND past_word = %s
            ORDER BY count DESC
            LIMIT 1;
            """,
            (
                username,
                past_word,
            ),
        )

        user_suggestions = [row[0] for row in cursor.fetchall()]
        suggestions = global_suggestions + user_suggestions

    except Exception as e:
        return JsonResponse(
            {"error": "failed to fetch suggestions.", "details": str(e)},
            status=500,
        )
    finally:
        if cursor:
            cursor.close()

    return JsonResponse({"suggestions": suggestions})


@api_view(["GET"])
def csrf_api(request):
    csrf_token = get_token(request)
    return JsonResponse({"csrf": csrf_token})


@api_view(["POST"])
def signup_api(request):
    if request.content_type != "application/json":
        return JsonResponse(
            {"error": "invalid content type. expected application/json."}, status=400
        )

    uname = request.data.get("username")
    email = request.data.get("email")
    pass1 = request.data.get("password1")
    pass2 = request.data.get("password2")
    name = request.data.get("name")
    age = request.data.get("age")

    if not all([uname, email, pass1, pass2, name, age]):
        return JsonResponse({"error": "all fields are required."}, status=400)

    if pass1 != pass2:
        return JsonResponse({"error": "passwords do not match."}, status=400)

    if User.objects.filter(username=uname).exists():
        return JsonResponse({"error": "username already exists."}, status=400)

    try:
        save_user(get_global_db_connection(), name, uname, pass1, email, age)

        my_user = User.objects.create_user(username=uname, email=email, password=pass1)
        my_user.save()

    except Exception as e:
        return JsonResponse(
            {"error": "registration failed.", "details": str(e)},
            status=500,
        )

    return JsonResponse({"message": "registered successfully."}, status=201)


@api_view(["POST"])
def login_api(request):
    if request.content_type != "application/json":
        return JsonResponse(
            {"error": "invalid content type. expected application/json."}, status=400
        )

    username = request.data.get("username")
    pass1 = request.data.get("pass")

    if not username:
        return JsonResponse({"error": "username is required."}, status=400)

    if not pass1:
        return JsonResponse({"error": "password is required."}, status=400)

    user = authenticate(request, username=username, password=pass1)
    if user is None:
        return JsonResponse({"error": "username or password is incorrect."}, status=403)

    login(request, user)

    return JsonResponse({"message": "logged in successfully."}, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logout_api(request):
    logout(request)
    return JsonResponse({"message": "logged out successfully."}, status=200)
