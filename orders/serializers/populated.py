from rest_framework import serializers

from jwt_auth.serializers import UserSerializer
from .common import OrderSerializer

class PopulatedOrderSerializer(OrderSerializer):
    buyer = UserSerializer()
    # product = ProductSerializer - when product model done 