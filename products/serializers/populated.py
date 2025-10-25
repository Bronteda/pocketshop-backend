from products.serializers.common import ProductSerializer
from jwt_auth.serializers import UserSerializer
from shops.serializers.populated import PopulatedShopSerializer
from orders.serializers.populated import PopulatedOrderSerializer


class PopulatedProductSerializer(ProductSerializer):
    owner = UserSerializer()
    shop = PopulatedShopSerializer()

class ProductWithOrdersSerializer(ProductSerializer):
    """
    Serializer for representing a product along with all its associated orders.
    """
    orders = PopulatedOrderSerializer(many=True)