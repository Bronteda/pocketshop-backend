from rest_framework import serializers
from products.models import Product, ProductImage


class IncomingProductImageSerializer(serializers.Serializer):
    public_id = serializers.CharField()
    # Accept either secure_url (new uploads from Cloudinary) or url (existing images being kept)
    secure_url = serializers.URLField(required=False)
    url = serializers.URLField(required=False)

    def validate(self, data):
        # Ensure at least one URL field is provided
        if not data.get('secure_url') and not data.get('url'):
            raise serializers.ValidationError(
                "Either 'secure_url' or 'url' must be provided")
        # Normalize: if both provided, prefer secure_url; otherwise use whichever is present
        if not data.get('url'):
            data['url'] = data.get('secure_url')
        return data


class ProductSerializer(serializers.ModelSerializer):
    images = IncomingProductImageSerializer(
        many=True, write_only=True, required=False)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'
