from django.db import models
from jwt_auth.models import User


class Shop(models.Model):
    def __str__(self):
        return f'{self.name} by {self.owner}'
    owner = models.OneToOneField(
        User,
        related_name="shop",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=50)
    bio = models.TextField()
    shop_image = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
