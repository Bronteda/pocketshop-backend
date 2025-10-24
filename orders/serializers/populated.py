from jwt_auth.serializers import UserSerializer
from orders.serializers.common import OrderSerializer
from products.serializers.common import ProductSerializer

class PopulatedOrderSerializer(OrderSerializer):
    buyer = UserSerializer()
    product = ProductSerializer()