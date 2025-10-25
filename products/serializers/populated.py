from products.serializers.common import ProductSerializer
from jwt_auth.serializers import UserSerializer
from shops.serializers.populated import PopulatedShopSerializer
from orders.serializers.populated import PopulatedOrderSerializer


class PopulatedProductSerializer(ProductSerializer):
    owner = UserSerializer()
    shop = PopulatedShopSerializer()

class ProductWithOrdersSerializer(ProductSerializer):
    orders = PopulatedOrderSerializer(many=True)