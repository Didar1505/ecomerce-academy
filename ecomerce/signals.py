from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order

from django.contrib.auth.models import User
from .models import Customer
from .mailer import EmailSender

@receiver(post_save, sender=Order)
def send_notification(sender, instance, created, **kwargs):
    if not created and instance.status == 'delivered':
        items_details = ""
        for item in instance.items.all():
            if item.product and item.product.seller:
                seller = item.product.seller
                seller.balance += item.get_cost()
                seller.save()
                items_details += f"- {item.product.title}: {item.quantity} x {item.product.price} = {item.get_cost()}\n"
        
        if instance.client and instance.client.user.email:
            total_cost = instance.get_total_cost()
            subject = f"Order Delivered - Order #{instance.id}"
            body = (
                f"Hello {instance.client.user.username},\n\n"
                f"Your order has been delivered!\n\n"
                f"Order Details:\n{items_details}\n"
                f"Total Cost: {total_cost}\n\n"
                f"Thank you for shopping with us!"
            )
            mailer = EmailSender()
            mailer.send(instance.client.user.email, subject, body)

@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.get_or_create(user=instance)