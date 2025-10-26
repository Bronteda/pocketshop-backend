# pylint: disable=no-member
from .serializers.common import ProductSerializer
from .serializers.populated import PopulatedProductSerializer
from .serializers.populated import ProductWithOrdersSerializer
from .models import Product
from shops.models import Shop

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.exceptions import NotFound


# This returns all the products (no auth)
class ProductListView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, _request):
        try:
            products = Product.objects.all()

            if not products.exists():
                return Response({"message": "No products found in db"}, status=status.HTTP_404_NOT_FOUND)

            serialized_products = PopulatedProductSerializer(
                products, many=True)
            return Response(serialized_products.data, status=status.HTTP_200_OK)

        except Exception as e:
            print("Error: ", {e})
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def post(self, request):
        try:
            shop = Shop.objects.get(owner=request.user)
        except Shop.DoesNotExist:
            return Response({"Error": "Shop Not Found in DB"}, status=status.HTTP_404_NOT_FOUND)
        print("shop is:", shop)

        request.data['owner'] = request.user.id
        request.data['shop'] = shop.id
        product_serializer = ProductSerializer(data=request.data)
        print("product_serializer:", product_serializer)

        try:
            product_serializer.is_valid(raise_exception=True)
            # Extract images from validated_data before saving product
            images_data = product_serializer.validated_data.pop("images", [])
            product = product_serializer.save()

            # Create ProductImage rows for each image
            for img in images_data:
                product.images.create(
                    public_id=img["public_id"],
                    url=img["secure_url"],
                    is_primary=img.get("is_primary", False)
                )

            # Return the fully populated product (includes images, shop, owner)
            populated = PopulatedProductSerializer(product)
            return Response(populated.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error: ", {e})
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)


# View a Product detail page
class ProductDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_product(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound("🆘 Can't find that Product")

    # GET/SHOW Product
    def get(self, _request, pk):
        product = self.get_product(pk=pk)
        serialized_product = PopulatedProductSerializer(product)
        return Response(serialized_product.data, status=status.HTTP_200_OK)

    # PUT/UPDATE Product
    def put(self, request, pk):
        product_to_update = self.get_product(pk=pk)

        if product_to_update.owner != request.user:
            return Response({"Error": "You do not have permissions to do that."}, status=status.HTTP_403_FORBIDDEN)

        request.data['owner'] = request.user.id
        request.data['shop'] = product_to_update.shop.id

        updated_product = ProductSerializer(
            product_to_update, data=request.data)

        try:
            # Validate payload first
            print("updated product is:", updated_product)
            updated_product.is_valid(raise_exception=True)

            # Extract images from validated_data before saving product
            images_data = updated_product.validated_data.pop("images", [])

            # Save Product 
            product = updated_product.save()

            # Create ProductImage rows for each image
            for img in images_data:
                    product.images.create(
                    public_id=img["public_id"],
                    url=img["secure_url"],
                    is_primary=img.get("is_primary", False)
                )

            # Return the fully populated product (includes images, shop, owner)
            populated = PopulatedProductSerializer(product)

            return Response(populated.data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print("Error: ", {e})
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # Note: errors are handled via raise_exception=True above and by the except block

    # DELETE Product
    def delete(self, request, pk):
        product_to_delete = self.get_product(pk=pk)

        if product_to_delete.owner != request.user:
            return Response({"Error": "You do not have permissions to do that."}, status=status.HTTP_403_FORBIDDEN)

        product_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # this is needed when quantity changes after order created
    def patch(self, request, pk):
        product_to_update = self.get_product(pk=pk)

        updated_product = ProductSerializer(
            product_to_update,
            data=request.data,
            partial=True
        )

        if updated_product.is_valid():
            updated_product.save()
            return Response(updated_product.data, status=status.HTTP_200_OK)

        return Response(updated_product.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


# View a product and its orders (Auth only)
class ProductOrdersView(APIView):
    permission_classes = (IsAuthenticated, )

    def get_product(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound("🆘 Can't find that Product")

    # GET/SHOW Product with orders
    def get(self, request, pk):
        product = self.get_product(pk=pk)

        if product.owner != request.user:
            return Response({"Error": "You do not have permissions to do that."}, status=status.HTTP_403_FORBIDDEN)

        serialized_product = ProductWithOrdersSerializer(product)
        return Response(serialized_product.data, status=status.HTTP_200_OK)