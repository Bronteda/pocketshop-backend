from django.db import models
from jwt_auth.models import User
# from products.models import Product


class Order(models.Model):
    def __str__(self):
        return f'Order {self.id} - Buyer: {self.buyer}'# Maybe change this to product when model done
    buyer = models.ForeignKey(
        User,
        related_name='orders',
        on_delete=models.CASCADE
    )
    # product = models.ForeignKey(
    #     Product,
    #     related_name='orders',
    #     on_delete=models.CASCADE
    # )
    status = models.CharField(max_length=50)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
