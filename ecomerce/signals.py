from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order

@receiver(post_save, sender=Order)
def send_notification(sender, instance, created, **kwargs):
    if created:
        print(f"client {instance.client.username} create order from \
              {instance.seller.user.username}")