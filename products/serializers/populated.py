from products.serializers.common import ProductSerializer, ProductImageSerializer
from jwt_auth.serializers import UserSerializer
from shops.serializers.populated import PopulatedShopSerializer


class PopulatedProductSerializer(ProductSerializer):
    owner = UserSerializer()
    shop = PopulatedShopSerializer()
    images = ProductImageSerializer(many=True, read_only=True)

