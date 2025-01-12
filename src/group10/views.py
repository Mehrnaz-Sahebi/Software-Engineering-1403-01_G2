from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import HttpResponse, redirect, render

from database.query import create_db_connection, save_user
from database.secret import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

# Create your views here.


def home(request):
    return render(request, "group10.html", {"group_number": "10"})


def suggest(request):
    past_word = request.GET.get("past_word")
    if past_word:
        mydb = create_db_connection(
            DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
        )
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

        except Exception as e:
            return HttpResponse("Error fetching suggestions")
        finally:
            cursor.close()
            mydb.close()

    return render(
        request,
        context={
            "suggestions": suggestions,
        },
    )

def SignupPage(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        email = request.POST.get("email")
        pass1 = request.POST.get("password1")
        pass2 = request.POST.get("password2")
        name = request.POST.get("name")
        age = request.POST.get("age")

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

    return render(request, "registration/signup.html")


def LoginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        pass1 = request.POST.get("pass")
        user = authenticate(request, username=username, password=pass1)

        if user is not None:
            login(request, user)
            return redirect("group10:home")
        else:
            return HttpResponse("Username or Password is incorrect!!!")

    return render(request, "registration/login.html")


def LogoutPage(request):
    logout(request)
    return redirect("group10:login")
