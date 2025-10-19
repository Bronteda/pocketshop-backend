from carts.serializers.common import CartSerializer
from jwt_auth.serializers import UserSerializer
from products.serializers.common import ProductSerializer


class PopulatedCartSerializer(CartSerializer):
    owner = UserSerializer()
    products = ProductSerializer(many=True)
