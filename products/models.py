from django.db import models
from jwt_auth.models import User
from shops.models import Shop


class Product(models.Model):
    def __str__(self):
        return f'''
                owner: {self.owner},
                shop: {self.shop},
                product_image: {self.product_image},
                title: {self.title},
                description: {self.description},
                price: {self.price},
                quantity: {self.quantity},
                category: {self.category},
                created_at: {self.created_at},
                updated_at: {self.updated_at}
                '''
    owner = models.ForeignKey(
        User,
        related_name="products",
        on_delete=models.CASCADE
    )
    shop = models.ForeignKey(
        Shop,
        related_name="products",
        on_delete=models.CASCADE
    )
    product_image = models.CharField(max_length=250)
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # ST: This will only allow positive numbers or zero
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Category(models.TextChoices):
        # Category.ART.value == "ART", Category.ART.label == "Art & Crafts"
        # DB will store the value and that's how we query/submit
        ART = "ART", "Art & Crafts"
        VINTAGE = "VINT", "Vintage"
        FASHION = "FASH", "Fashion"
        HOME = "HOME", "Home & Living"
        BEAUTY = "BEAU", "Beauty & Personal Care"
        ELECTRONICS = "ELEC", "Electronics & Gadgets"
        PETS = "PETS", "Pet Supplies"
        DIGITAL = "DIGI", "Digital Goods"
        SPORTS = "SPRT", "Sports & Outdoors"
        CUSTOM = "CUST", "Custom Orders"

    category = models.CharField(
        max_length=4,
        choices=Category.choices,
        default=Category.CUSTOM
    )
