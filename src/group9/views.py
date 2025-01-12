from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import get_user_model
from registration.database.secret import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from group9.database.query import *
from django.db import IntegrityError
from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.models import User

def home(request):
    return render (request , 'group9.html' , {'group_number': '9'})


def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        name = request.POST.get('name')
        age = request.POST.get('age')

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not the same!")
        else:
            if User.objects.filter(username=uname).exists():
                return HttpResponse("This username is already taken. Please choose another one.")
            try:
                my_user = User.objects.create_user(uname, email, pass1)
                print('User created:', my_user)
                
                my_user.save()
                mydb = create_db_connection(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
                save_user(mydb, name, uname, pass1, email, age)
                return redirect('login')
            except IntegrityError:
                return HttpResponse("An error occurred while creating your account. Please try again.")
    
    return render(request, 'group9/signup.html')


def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        print(user)
        print(username)
        print(pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'group9/login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')