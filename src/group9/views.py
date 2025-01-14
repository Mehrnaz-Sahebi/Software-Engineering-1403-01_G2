from django.shortcuts import render, redirect, HttpResponse
from registration.database.secret import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from registration.database.query import *
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from group9.logic import optimize_text, fetch_user_history
from django.contrib.auth.models import User


def home(request):
    """
    This view renders the homepage of the application.

    It simply returns a response rendering the 'group9.html' template.
    The template is passed a dictionary with the key 'group_number', which holds the group number (9) to display on the page.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A response rendering the homepage template with the group number information.
    """
    return render(request, "group9.html", {"group_number": "9"})


def SignupPage(request):
    """
    This view handles the user registration (signup) process.

    If the HTTP request method is POST, it means the user has submitted the registration form. The view extracts the submitted data:
    - Username, email, password1, password2, name, and age from the form.
    It checks if the passwords match, and if the username is already taken. If there are any issues, the function will return appropriate error messages.

    If everything is valid, a new user is created using Django's `create_user` method. After saving the user to the system, the user details are also stored in the custom database using the `save_user` function.

    If the user is created successfully, they are redirected to the login page. If there are any errors during the process, an appropriate error message is displayed.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A response rendering the signup template or redirecting to the login page if registration is successful.
    """
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
                print("User created:", my_user)
                my_user.save()
                mydb = create_db_connection(
                    DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
                )
                save_user(mydb, name, uname, pass1, email, age)
                return redirect("group9:login")
            except IntegrityError:
                return HttpResponse(
                    "An error occurred while creating your account. Please try again."
                )

    return render(request, "group9/signup.html")


def LoginPage(request):
    """
    This view handles user login.

    If the HTTP request method is POST, it means the user has submitted the login form. The view retrieves the submitted username and password.
    It uses Django's `authenticate` function to verify the user's credentials.
    If the credentials are valid, the user is logged in and redirected to the optimize page.

    If the login fails, an error message is shown.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A response rendering the login template or redirecting to the optimize page if login is successful.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        pass1 = request.POST.get("pass")
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect("group9:optimize")
        else:
            return HttpResponse("Username or Password is incorrect!!!")
    return render(request, "group9/login.html")


def LogoutPage(request):
    """
    This view handles user logout.

    When the user clicks logout, this view will log them out and redirect to the login page.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A response redirecting to the login page after successful logout.
    """
    logout(request)
    return redirect("group9:login")


# @login_required
def OptimizePage(request):
    """
    This view handles the text optimization process.

    If the HTTP request method is POST, it means the user has submitted the optimization form.
    The view retrieves the text input and the user preferences for different normalization options (e.g., correct spacing, remove diacritics, etc.).
    The `optimize_text` function is then called with the provided input text and options, which applies the normalization based on the user's preferences.

    After the text is optimized, the result is rendered and displayed on the optimize page.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A response rendering the optimize template with the optimized text or the original text if it's a GET request.
    """
    if request.method == "POST":
        # Extract form data from POST request
        input_text = request.POST.get("input", "")
        correct_spacing = request.POST.get("correct_spacing") == "on"
        remove_diacrities = request.POST.get("remove_diacrities") == "on"
        remove_special_chars = request.POST.get("remove_special_chars") == "on"
        decrease_repeated_chars = request.POST.get("decrease_repeated_chars") == "on"
        persian_style = request.POST.get("persian_style") == "on"
        persian_number = request.POST.get("persian_number") == "on"
        unicodes_replacement = request.POST.get("unicodes_replacement") == "on"
        seperate_mi = request.POST.get("seperate_mi") == "on"
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
            db_connection=mydb,
        )

        # Render the template with the result
        return render(
            request,
            "group9/optimize.html",
            {"optimized_text": optimized_text, "input_text": input_text},
        )

    # For GET requests, just render the empty form
    return render(request, "group9/optimize.html")


def HistoryPage(request):
    """
    This view retrieves and displays the user's history of mistakes.

    The view first checks if the user is authenticated. If not, they are redirected to the login page.
    If the user is authenticated, their history of mistakes (from the previous optimization sessions) is fetched using the `fetch_user_history` function.
    The mistakes are then rendered on the history page for the user to review.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A response rendering the history page with the user's previous mistakes.
    """
    if not request.user.is_authenticated:
        return redirect("group9:login")

    user = str(request.user.username)
    print(user)
    db_connection = create_db_connection(
        DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
    )

    # Fetch history using logic function
    user_history = fetch_user_history(user, db_connection)
    print(user_history)
    return render(request, "group9/history.html", {"mistakes": user_history})
