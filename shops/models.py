from django.db import models
from jwt_auth.models import User


class Shop(models.Model):
    def __str__(self):
        return f'''
                owner: {self.owner},
                name: {self.name},
                bio: {self.bio},
                shop_image: {self.shop_image},
                created_at: {self.created_at},
                updated_at: {self.updated_at}
                '''
    owner = models.OneToOneField(
        User,
        related_name="shop",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=50)
    bio = models.TextField()
    # ST: shop_image should be optional / added later
    shop_image = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
