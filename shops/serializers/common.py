from rest_framework import serializers
from shops.models import Shop


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'
        # Changed to remove owner as read_only because it was preventing postman creates
        read_only_fields = ("created_at", "updated_at")