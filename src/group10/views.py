import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import HttpResponse, redirect, render
from django.http import JsonResponse

from database.query import create_db_connection, save_user
from database.secret import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

# Create your views here.


def HomePage(request):
    return render(request, "index.html")


def Suggest(request):
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
        except IntegrityError:
            return HttpResponse("Error fetching suggestions.")
        finally:
            cursor.close()
            mydb.close()

    suggestions_data = [
        {"current_word": word, "probability": prob} for word, prob in suggestions
    ]
    return JsonResponse({"suggestions": suggestions_data})


def SignupPage(request):
    if request.method == "POST":
        data = json.loads(request.body)

        uname = data.get("username")
        email = data.get("email")
        pass1 = data.get("password1")
        pass2 = data.get("password2")
        name = data.get("name")
        age = data.get("age")

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not the same!")
        else:
            if User.objects.filter(username=uname).exists():
                return HttpResponse(
                    "This username is already taken. Please choose another one."
                )
            try:
                my_user = User.objects.create_user(uname, email, pass1)
                my_user.save()
                mydb = create_db_connection(
                    DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
                )
                save_user(mydb, name, uname, pass1, email, age)

                return redirect("group10:login")
            except IntegrityError:
                return HttpResponse(
                    "An error occurred while creating your account. Please try again."
                )

    return render(request, "signup.html")


def LoginPage(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data.get("username")
        pass1 = data.get("pass")

        user = authenticate(request, username=username, password=pass1)

        if user is not None:
            login(request, user)
            return redirect("group10:home")
        else:
            return HttpResponse("Username or Password is incorrect.", status=403)

    return render(request, "login.html")


def LogoutPage(request):
    logout(request)
    return redirect("group10:login")
