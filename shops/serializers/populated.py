from shops.serializers.common import ShopSerializer
from jwt_auth.serializers import UserSerializer
from products.serializers.populated import PopulatedProductSerializer


class PopulatedShopSerializer(ShopSerializer):
    owner = UserSerializer()
    # This will return products:[{}] in the response
    products = PopulatedProductSerializer(many=True)