from decimal import Decimal
from django.db import models
from jwt_auth.models import User
from products.models import Product


class Cart(models.Model):
    def __str__(self):
        return f"Cart for {self.owner.username}"
    owner = models.OneToOneField(
        User,
        related_name="cart",
        on_delete=models.CASCADE
    )
    products = models.ManyToManyField(
        Product,
        related_name="carts",
        default= None
    )
    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )
