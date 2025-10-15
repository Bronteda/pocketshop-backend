from django.db import models
from django.contrib.auth.models import AbstractUser 

class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    profile_image = models.CharField(max_length=300)
