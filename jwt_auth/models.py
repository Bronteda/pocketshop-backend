from django.db import models
from django.contrib.auth.models import AbstractUser 

class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    # Changing to default address to null,blank since we don't ask for it during sign up
    address = models.CharField(max_length=150, null=True, blank=True)
    profile_image = models.CharField(max_length=300, null=True, blank=True)
