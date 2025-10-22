from carts.serializers.common import CartSerializer, CartItemSerializer
from jwt_auth.serializers import UserSerializer
from products.serializers.common import ProductSerializer



class PopulatedCartItemSerializer(CartItemSerializer):
    product = ProductSerializer()


class PopulatedCartSerializer(CartSerializer):
    owner = UserSerializer() 
    cart_items = PopulatedCartItemSerializer(many=True, read_only=True)
