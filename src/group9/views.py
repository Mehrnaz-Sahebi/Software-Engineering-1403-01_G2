from django.shortcuts import render, redirect, HttpResponse
from registration.database.secret import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from registration.database.query import *
from django.db import IntegrityError
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from group9.logic import optimize_text,fetch_user_history
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
                return redirect('group9:login')
            except IntegrityError:
                return HttpResponse("An error occurred while creating your account. Please try again.")
    
    return render(request, 'group9/signup.html')


def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        print(user.email)
        print(username)
        print(pass1)
        if user is not None:
            login(request,user)  
            return redirect('group9:optimize')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")
    return render (request,'group9/login.html')


def LogoutPage(request):
    logout(request)
    return redirect('login')


# @login_required
def OptimizePage(request):
    if request.method == 'POST':
        # Extract form data from POST request
        input_text = request.POST.get('input', '')
        correct_spacing = request.POST.get('correct_spacing') == 'on'
        remove_diacrities = request.POST.get('remove_diacrities') == 'on'
        remove_special_chars = request.POST.get('remove_special_chars') == 'on'
        decrease_repeated_chars = request.POST.get('decrease_repeated_chars') == 'on'
        persian_style = request.POST.get('persian_style') == 'on'
        persian_number = request.POST.get('persian_number') == 'on'
        unicodes_replacement = request.POST.get('unicodes_replacement') == 'on'
        seperate_mi = request.POST.get('seperate_mi') == 'on'
        mydb = create_db_connection(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
        # Call the optimize_text function
        optimized_text = optimize_text(
            input=input_text,
            user=request.user,
            correct_spacing=correct_spacing,
            remove_diacrities=remove_diacrities,
            remove_special_chars=remove_special_chars,
            decrease_repeated_chars=decrease_repeated_chars,
            persian_style=persian_style,
            persian_number=persian_number,
            unicodes_replacement=unicodes_replacement,
            seperate_mi=seperate_mi,
            db_connection=mydb
        )

        # Render the template with the result
        return render(request, 'group9/optimize.html', {'optimized_text': optimized_text, 'input_text': input_text})

    # For GET requests, just render the empty form
    return render(request, 'group9/optimize.html')



def HistoryPage(request):
    if not request.user.is_authenticated:
        return redirect('group9:login')  # Redirect to login if the user is not authenticated

    # print(f"Authenticated User: {request.user}")  # Debugging the user object
    # print(f"User ID: {request.user.id}") 
    user =str( request.user.username)
    print(user)
    db_connection = create_db_connection(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)

    # Fetch history using logic function
    user_history = fetch_user_history(user, db_connection)
    print(user_history)
    # return render(request, 'group9/history.html', {'history': user_history})
    return render(request, 'group9/history.html', {'mistakes': user_history})

