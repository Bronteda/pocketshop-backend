from carts.serializers.common import CartSerializer, CartItemSerializer
from jwt_auth.serializers import UserSerializer
from products.serializers.populated import PopulatedProductSerializer



class PopulatedCartItemSerializer(CartItemSerializer):
    product = PopulatedProductSerializer()


class PopulatedCartSerializer(CartSerializer):
    owner = UserSerializer() 
    cart_items = PopulatedCartItemSerializer(many=True, read_only=True)
