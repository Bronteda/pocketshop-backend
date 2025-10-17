from products.serializers.common import ProductSerializer
from jwt_auth.serializers import UserSerializer
from shops.serializers.populated import PopulatedShopSerializer


class PopulatedProductSerializer(ProductSerializer):
    owner = UserSerializer()
    shop = PopulatedShopSerializer()
