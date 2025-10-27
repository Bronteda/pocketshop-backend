from rest_framework import serializers
from products.models import Product, ProductImage


class IncomingProductImageSerializer(serializers.Serializer):
    public_id = serializers.CharField()
    secure_url = serializers.URLField()


class ProductSerializer(serializers.ModelSerializer):
    images = IncomingProductImageSerializer(many=True, write_only=True, required=False)
    class Meta:
        model = Product
        fields = '__all__'



class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'
        