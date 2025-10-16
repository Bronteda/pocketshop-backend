from shops.serializers.common import ShopSerializer
from jwt_auth.serializers import UserSerializer


class PopulatedShopSerializer(ShopSerializer):
    owner = UserSerializer()
