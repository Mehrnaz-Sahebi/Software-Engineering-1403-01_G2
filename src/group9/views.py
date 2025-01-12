import os

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import get_user_model
from group9.database.secret import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from group9.database.query import *
from django.db import IntegrityError
from django.contrib.auth import authenticate,login,logout

User = get_user_model()

def home(request):
    return render (request , 'group9.html' , {'group_number': '9'})


def signup_page(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')  
        last_name = request.POST.get("last_name")
        phone_number = request.POST.get("phone_number")

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not the same!")
        else:
            # بررسی نام کاربری برای جلوگیری از تکرار
            if User.objects.filter(username=uname).exists():
                return HttpResponse("This username is already taken. Please choose another one.")
            try:
                my_user = User.objects.create_user(uname, email, pass1, first_name, last_name, phone_number)
                # اینجا می‌توانید اطلاعات اضافی مانند 'name' و 'age' را در پروفایل کاربر ذخیره کنید
                print('User created:', my_user)
                my_user.save()
                mydb = create_db_connection(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
                save_user(mydb, uname, pass1, email, first_name, last_name, phone_number)
                return redirect('login')
            except IntegrityError:
                return HttpResponse("An error occurred while creating your account. Please try again.")
    
    return render(request, 'group9/signup.html')


def login_page(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'group9/login.html')


def logout_page(request):
    logout(request)
    return redirect('login')


def dynamic_view(request, path):
    #TODO: check if dir exists/create a good 404 page

    path = os.path.join('group9/templates', path)
    if path.endswith('/'):
        return handle_directory(request, path)
    else:
        return handle_file(request, path)



def handle_directory(request, path):
    path = os.path.abspath(path)
    template_path = os.path.join(path, f'{os.path.basename(path)}.html')
    return render(request, template_path)


def handle_file(request, path):
    return render(request, os.path.abspath(path))