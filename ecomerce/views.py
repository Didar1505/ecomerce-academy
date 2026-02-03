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

@login_required
def profile(request):
    return render(request, "ecomerce/profile.html")

@login_required
def update_profile(request):
    if request.method == "POST":
        user = request.user
        # Update User fields
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        
        full_name = request.POST.get("full_name", "").strip()
        if " " in full_name:
            user.first_name, user.last_name = full_name.split(" ", 1)
        else:
            user.first_name = full_name
            user.last_name = ""
        user.save()

        # Update Customer fields
        customer = user.customer
        customer.phone = request.POST.get("phone")
        customer.address = request.POST.get("address")
        if request.FILES.get("image"):
            customer.image = request.FILES["image"]
        customer.save()
        return redirect("profile")
        
    return render(request, "ecomerce/profile_update.html")

@login_required
def my_orders(request):
    orders = models.Order.objects.filter(client=request.user.customer).order_by("-created_at")
    return render(request, "ecomerce/my_orders.html", {"orders": orders})

@login_required
def add_order_item(request, id):
    customer = request.user.customer
    order, created = models.Order.objects.get_or_create(client=customer, status='pending')
    if request.method == "POST":
        product = models.Product.objects.get(id=id)
        qty = int(request.POST.get("quantity", 1))
        order_item, created = models.OrderItem.objects.get_or_create(order=order, product=product)
        if not created:
            order_item.quantity += qty
        else:
            order_item.quantity = qty
        order_item.save()
    return redirect("index")

@login_required
def confirm_order(request, order_id):
    order = models.Order.objects.get(id=order_id, client=request.user.customer)
    if request.method == "POST":
        order.status = 'delivered'  # or appropriate status update
        order.save()
    return redirect("my_orders")