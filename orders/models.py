from django.db import models
from jwt_auth.models import User
from products.models import Product
from payments.models import Payment


class Order(models.Model):
    def __str__(self):
        return f'''
                buyer: {self.buyer},
                product: {self.product},
                status: {self.status},
                subtotal: {self.subtotal},
                quantity: {self.quantity},
                created_at: {self.created_at},
                updated_at: {self.updated_at}
                '''
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
    payment = models.ForeignKey(
        Payment,
        related_name='orders',
        on_delete=models.CASCADE,  # ST: Updating to delete from protect

        # ST: maybe we should update to require payment for order, if order cannot be created before payment is provided
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # ST: Changing to (auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    '''
    auto_now_add=True sets the timestamp only once when the row is created (good for created_at).
    auto_now=True updates the timestamp every time model.save() is called (good for updated_at).
    '''
