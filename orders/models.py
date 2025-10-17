from django.db import models
from jwt_auth.models import User
from products.models import Product


class Order(models.Model):
    def __str__(self):
        return f'Order {self.id} - Buyer: {self.buyer}'
    buyer = models.ForeignKey(
        User,
        related_name='orders',
        on_delete=models.CASCADE
    )
    product = models.OneToOneField(
			Product,
			related_name="order",
			on_delete=models.CASCADE
	)
    status = models.CharField(max_length=50)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    # payment = models.ForeignKey(
    #     Payment,
    #     related_name='orders',
    #     on_delete=models.PROTECT, # prevent deleting a Payment that has Orders
    #     null=True,
    #     blank=True
    # )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
