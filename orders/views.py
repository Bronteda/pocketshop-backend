from .models import Order
from .serializers.common import OrderSerializer
from .serializers.populated import PopulatedOrderSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

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
            orders_to_add.is_valid()
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

        if order_to_update.buyer != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        request.data["buyer"] = request.user.id
        print(request.data)

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