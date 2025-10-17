from shops.serializers.common import ShopSerializer
from jwt_auth.serializers import UserSerializer
from products.serializers.common import ProductSerializer


class PopulatedShopSerializer(ShopSerializer):
    owner = UserSerializer()
    # This will return products:[{}] in the response
    products = ProductSerializer(many=True)