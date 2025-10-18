from django.db import models
from jwt_auth.models import User


# Unsure if we need statuses, keep for now
class PaymentStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    SUCCEEDED = "SUCCEEDED", "Succeeded"
    FAILED = "FAILED", "Failed"

# We can add a currency selection later if we want to support more than USD
# Amount is not needed for MVP because we're only validating expiration date


class Payment(models.Model):
    def __str__(self):
        return f'''
                owner: {self.owner},
                currency: {self.currency},
                status: {self.status},
                provider: {self.provider},
                payment_intent_id: {self.payment_intent_id},
                created_at: {self.created_at},
                updated_at: {self.updated_at}
                '''
    owner = models.ForeignKey(
        User,
        related_name="payments",
        on_delete=models.CASCADE,
    )
    currency = models.CharField(max_length=3, default="USD")
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )
    provider = models.CharField(max_length=32, default="mockpay")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Generate a fake payment_intent_id in mock service payment
    payment_intent_id = models.CharField(max_length=80, default="test_id")
