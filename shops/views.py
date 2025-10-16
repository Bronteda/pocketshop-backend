# pylint: disable=no-member
from rest_framework.views import APIView  # main API controller class
from rest_framework.response import Response  # response class
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.exceptions import NotFound
from .serializers.common import ShopSerializer
from .serializers.populated import PopulatedShopSerializer
from .models import Shop


class ShopListView(APIView):
    # This should allow GET requests from unauth, but protect POST,PUT,DELETE routes from unauth
    permission_classes = (IsAuthenticatedOrReadOnly, )

    # This returns all shops (no auth)
    def get(self, _request):
        shops = Shop.objects.all()
        serialized_shops = ShopSerializer(shops, many=True)
        return Response(serialized_shops.data, status=status.HTTP_200_OK)

    # Creating a shop requires Authentication
    def post(self, request):
        request.data['owner'] = request.user.id
        shop_to_add = ShopSerializer(data=request.data)
        print("shop_to_add:", shop_to_add)
        try:
            shop_to_add.is_valid(raise_exception=True)
            shop_to_add.save()
            return Response(shop_to_add.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print('ERROR')
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ShopDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_shop(self, pk):
        try:
            return Shop.objects.get(pk=pk)
        except Shop.DoesNotExist:
            raise NotFound(detail="🆘 Can't find that Shop")

    # GET/VIEW Shop
    def get(self, _request, pk):
        shop = self.get_shop(pk=pk)
        serialized_shop = PopulatedShopSerializer(shop)
        return Response(serialized_shop.data, status=status.HTTP_200_OK)

    # PUT/UPDATE Shop
    def put(self, request, pk):
        shop_to_update = self.get_shop(pk=pk)
        print('request.user:', request.user)
        if shop_to_update.owner != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        updated_shop = ShopSerializer(shop_to_update, data=request.data)
        if updated_shop.is_valid():
            updated_shop.save()
            return Response(updated_shop.data, status=status.HTTP_202_ACCEPTED)

        return Response(updated_shop.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    # DELETE Shop
    def delete(self, request, pk):
        shop_to_delete = self.get_shop(pk=pk)

        if shop_to_delete.owner != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        shop_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
