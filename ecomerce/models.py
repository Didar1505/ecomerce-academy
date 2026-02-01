from django.db import models
from django.contrib.auth.models import User

class Seller(models.Model):
    POSITIONS = [
        ("seller", "Seller"),
        ("main_seller", "Main seller"),
        ("supervisor", "Supervisor")
    ]
    user = models.OneToOneField(User,null=True, on_delete=models.SET_NULL)
    phone = models.IntegerField(null=True, blank=True)
    work_date = models.DateTimeField(auto_now_add=True)
    position = models.CharField(max_length=250, choices=POSITIONS, default="seller")
    balance = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return self.user.username

class Product(models.Model):
    title = models.CharField(max_length=250)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Order(models.Model):
    client= models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    seller= models.ForeignKey(Seller,null=True, on_delete=models.SET_NULL)
    product= models.ManyToManyField(Product)
    created_at= models.DateTimeField(auto_now_add=True)
    total_cost= models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return str(self.created_at) + " " + self.client.username


