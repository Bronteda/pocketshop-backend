# pylint: disable=no-member
from .models import Order
from .serializers.common import OrderSerializer
from .serializers.populated import PopulatedOrderSerializer
from products.serializers.populated import PopulatedProductSerializer
from shops.models import Shop

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from collections import defaultdict
from rest_framework.permissions import IsAuthenticated
# IsAuthenticatedOrReadOnly specifies that a view is secure on all methods except get requests


class OrdersListView(APIView):
    permission_classes = (IsAuthenticated, )

    # Get all orders
    def get(self, request):
        try:
            orders = Order.objects.all()

            # If no orders in the db
            if not orders.exists():
                return Response({"message": "No orders found in db"}, status=status.HTTP_404_NOT_FOUND)

            serialized_orders = PopulatedOrderSerializer(orders, many=True)
            return Response(serialized_orders.data, status=status.HTTP_200_OK)

        except Exception as e:
            print("Error: ", {e})
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def post(self, request):
        request.data["buyer"] = request.user.id
        orders_to_add = OrderSerializer(data=request.data)
        
        try:
            print(orders_to_add)
            orders_to_add.is_valid(raise_exception=True)
            orders_to_add.save()
            return Response(orders_to_add.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error: ", e)
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class OrdersByBuyer(APIView):
    permission_classes = (IsAuthenticated, )

    # only able to see your own orders
    def get(self, request):
        try:
            print(request.user.id)
            # get all orders where the buyer/owner id matches the user id
            orders_by_owner = Order.objects.filter(buyer=request.user.id)

            # If user has no orders in the db
            if not orders_by_owner.exists():
                return Response({"message": "No orders found in db"}, status=status.HTTP_404_NOT_FOUND)

            serialized_orders_by_owner = PopulatedOrderSerializer(
                orders_by_owner, many=True)
            return Response(serialized_orders_by_owner.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("Error: ", {e})
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class OrderDetailView(APIView):
    permission_classes = (IsAuthenticated, )

    def get_order(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise NotFound(detail=f"Can't find Order with Primary Key {pk}")

    # Get Order details -  show page
    def get(self, request, pk):
        try:
            order = self.get_order(pk)
            serialized_order = PopulatedOrderSerializer(order)
            return Response(serialized_order.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("Error: ", {e})
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    # edit the order
    def put(self, request, pk):
        order_to_update = self.get_order(pk)

        if request.user not in (order_to_update.buyer, order_to_update.product.owner):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        request.data["payment"] = order_to_update.payment.id
        request.data["buyer"] = order_to_update.buyer.id
        request.data["product"] = order_to_update.product.id

        #have to keep it Common serializer otherwise it expects the full buyer dictionary
        serialized_updated_order = OrderSerializer(
            order_to_update, data=request.data)

        if serialized_updated_order.is_valid():
            serialized_updated_order.save()
            return Response(serialized_updated_order.data, status=status.HTTP_200_OK)

        return Response(serialized_updated_order.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        order_to_delete = self.get_order(pk)

        if order_to_delete.buyer != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        order_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# We need a view for getting all the orders of products FOR THIS SHOP
class OrdersForProductsByShop(APIView):
    permission_classes = (IsAuthenticated, )

    # get me all the orders associated with the products for this user's shop
    def get(self, request):
        try:
            shop = request.user.shop
            print("shop is:", shop)
        except Shop.DoesNotExist:
            return Response({"detail": "User has no shop"}, status=status.HTTP_404_NOT_FOUND)

        orders_qs = Order.objects.filter(product__shop=shop).select_related('product', 'buyer', 'payment')

        orders_by_product = defaultdict(list)
        for o in orders_qs:
            orders_by_product[o.product_id].append(o)

        # Only include products that actually have orders
        product_ids = list(orders_by_product.keys())
        if product_ids:
            # 'products' is your related_name
            products = shop.products.filter(id__in=product_ids).select_related('owner', 'shop')
        else:
            products = []

        response = []
        for p in products:
            product_data = PopulatedProductSerializer(p).data
            product_orders = orders_by_product.get(p.id, [])
            orders_data = PopulatedOrderSerializer(product_orders, many=True).data
            response.append({
                "product": product_data,
                "orders": orders_data
            })

        return Response(response, status=status.HTTP_200_OK)