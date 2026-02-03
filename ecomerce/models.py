from django.db import models
from django.contrib.auth.models import User

class Seller(models.Model):
    POSITIONS = [
        ("seller", "Seller"),
        ("main_seller", "Main seller"),
        ("supervisor", "Supervisor")
    ]
    user = models.OneToOneField(User,null=True, on_delete=models.SET_NULL)
    phone = models.CharField(max_length=50, null=True, blank=True)
    work_date = models.DateTimeField(auto_now_add=True)
    position = models.CharField(max_length=250, choices=POSITIONS, default="seller")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.user.username if self.user else "Unknown Seller"

class Product(models.Model):
    title = models.CharField(max_length=250)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]
    client= models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    seller= models.ForeignKey(Seller,null=True, on_delete=models.SET_NULL)
    created_at= models.DateTimeField(auto_now_add=True)
    total_cost= models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        client_name = self.client.username if self.client else "Unknown"
        return f"{self.created_at} {client_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_cost(self):
        return self.price * self.quantity
