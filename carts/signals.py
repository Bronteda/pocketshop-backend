#This is a signal file - it will create a cart when a user is registered 

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Cart

@receiver(post_save, sender=settings.AUTH_USER_MODEL) # means: after a user is saved, run this function.
def create_cart_for_new_user(sender, instance, created, **kwargs):
    if created: # ensures it only runs when a new user is created, not on every save.
        Cart.objects.create(owner=instance)