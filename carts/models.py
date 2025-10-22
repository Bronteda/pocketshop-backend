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
    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )


class CartItem(models.Model):
    # Multiple cart_items can be in Cart ? Is this ManyToMany
    cart = models.ForeignKey(
        Cart,
        related_name="cart_items",
        default=None,
        on_delete=models.PROTECT
    )
    # 1 cartItem per product (many products)
    product = models.ForeignKey(
        Product,
        related_name="cart_items",
        default=None,
        on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField(default=1)
