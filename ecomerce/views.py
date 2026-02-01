from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . import models

def index(request):
    products = models.Product.objects.all()

    return render(request, "ecomerce/index.html", {"products": products})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method=="POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("index")
        else:
            print("invalid credentials")
    return render(request, "ecomerce/login.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # redirect
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "ecomerce/register.html", {"form": form})

def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("login")