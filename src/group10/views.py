from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, "group10.html", {"group_number": "10"})


def suggest(request):
    return render(request, "group10.html", {"group_number": "10"})
