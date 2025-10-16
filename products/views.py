# pylint: disable=no-member
from .serializers.common import ProductSerializer
from .serializers.populated import PopulatedProductSerializer
from .models import Product
from shops.models import Shop

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.exceptions import NotFound


# This returns all the products (no auth)
class ProductListView(APIView):
    def get(self, _request):
        products = Product.objects.all()
        serialized_products = PopulatedProductSerializer(products, many=True)
        return Response(serialized_products.data, status=status.HTTP_200_OK)


# This view is to create a new product
class ProductCreateView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        try:
            shop = Shop.objects.get(owner=request.user)
        except Shop.DoesNotExist:
            return Response({"Error": "Shop Not Found in DB"}, status=status.HTTP_404_NOT_FOUND)
        print("shop is:", shop)

        request.data['owner'] = request.user.id
        request.data['shop'] = shop.id
        product_to_add = ProductSerializer(data=request.data)
        print("product_to_add:", product_to_add)

        try:
            product_to_add.is_valid(raise_exception=True)
            product_to_add.save()
            return Response(product_to_add.data, status=status.HTTP_201_CREATED)
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
            return Response({"Error": "You do not have permissions to do that."}, status=status.HTTP_401_UNAUTHORIZED)

        request.data['owner'] = request.user.id
        request.data['shop'] = product_to_update.shop.id

        updated_product = ProductSerializer(
            product_to_update, data=request.data)

        print("updated product is:", updated_product)

        if updated_product.is_valid():
            updated_product.save()
            return Response(updated_product.data, status=status.HTTP_202_ACCEPTED)

        return Response(updated_product.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    # DELETE Product
    def delete(self, request, pk):
        product_to_delete = self.get_product(pk=pk)

        if product_to_delete.owner != request.user:
            return Response({"Error": "You do not have permissions to do that."}, status=status.HTTP_401_UNAUTHORIZED)

        product_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Get all products by shop (ADD PRODUCTS to SHOP SERIALIZER)
