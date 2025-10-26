from products.serializers.common import ProductSerializer, ProductImageSerializer
from jwt_auth.serializers import UserSerializer
from shops.serializers.populated import PopulatedShopSerializer
from orders.serializers.populated import PopulatedOrderSerializer


class PopulatedProductSerializer(ProductSerializer):
    owner = UserSerializer()
    shop = PopulatedShopSerializer()
    images = ProductImageSerializer(many=True, read_only=True)


class ProductWithOrdersSerializer(ProductSerializer):
    """
    Serializer for representing a product along with all its associated orders.
    """
    orders = PopulatedOrderSerializer(many=True)
