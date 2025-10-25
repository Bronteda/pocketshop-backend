from rest_framework import serializers
from jwt_auth.serializers import UserSerializer
from orders.serializers.common import OrderSerializer
from products.serializers.populated import ProductSerializer


class PopulatedOrderSerializer(OrderSerializer):
    buyer = UserSerializer()
    # replace direct nested class with a method field
    product = serializers.SerializerMethodField()

    def get_product(self, obj):
        # local import prevents circular import at module load time
        from products.serializers.populated import PopulatedProductSerializer
        return PopulatedProductSerializer(obj.product).data