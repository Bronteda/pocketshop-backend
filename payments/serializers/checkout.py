from rest_framework import serializers
from datetime import date

class CheckoutSerializer(serializers.Serializer):
    # card_number = serializers.CharField(write_only=True)
    exp_month = serializers.IntegerField(write_only=True, min_value=1, max_value=12)
    exp_year = serializers.IntegerField(write_only=True)
    # cvc = serializers.CharField(write_only=True, min_length=3, max_length=4)

    def validate(self, data):
        today = date.today()

        card_expiry = date(data["exp_year"], data["exp_month"], 1)

        # validate expiry
        if (card_expiry.year < today.year) or (
            card_expiry.year == today.year and card_expiry.month <= today.month):
            raise serializers.ValidationError("Payment declined. Card is expired.")
        
        return data
    
