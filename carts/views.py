
from .serializers.common import CartSerializer, CartItemSerializer
from .serializers.populated import PopulatedCartSerializer
from carts.models import Cart, CartItem
from products.models import Product
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound


# Cart is created automatically when user registers (via signals.py)

class MyCartView(APIView):
    # Get or update the current user's cart
    permission_classes = [IsAuthenticated]

    # Get Auth users cart - One cart per user
    def get(self, request):
        try:
            cart = Cart.objects.get(owner=request.user)
            serialized_cart = PopulatedCartSerializer(cart)
            return Response(serialized_cart.data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response(
                {"detail": f"No cart found for user {request.user.username}"},
                status=status.HTTP_404_NOT_FOUND
            )

    # add product to cart
    # When you add a product you send in Product id and quantity
    # def post(self, request):
    #     try:
    #         # Find the user's cart
    #         cart = Cart.objects.get(owner=request.user)
    #         # Add product to cart (assuming product ID is sent in request.data)
    #         product_id = request.data.get("product")
    #         if not product_id:
    #             return Response({"detail": "Product ID required."}, status=status.HTTP_400_BAD_REQUEST)
    #         #Add product to cart
    #         cart.products.add(product_id)

    #         # #This is removing the quantity you are adding to your cart
    #         # quantity_of_product = request.data.get("quantity")
    #         # find_product = Product.objects.get(pk=product_id)
    #         # print("found product:", find_product)
    #         # find_product.quantity - quantity_of_product
    #         # Product.save()

    #         products_array = cart.products.all() #work out all products in cart
    #         #print(products_array)
    #         cart.total_cost = CalculateTotal(products_array)

    #         cart.save()
    #         # Serialize the updated cart
    #         serialized_cart = PopulatedCartSerializer(cart)
    #         return Response(serialized_cart.data, status=status.HTTP_200_OK)

    #     except Cart.DoesNotExist:
    #         raise NotFound(
    #             detail=f"Can't find Cart for user {request.user.username}")

    # #Remove product from cart
    # def delete(self, request):
        # try:
        #     cart = Cart.objects.get(owner=request.user)

        #     product_id = request.data.get("product")
        #     # Remove product from cart
        #     cart.products.remove(product_id)
        #     # work out all products in cart after action
        #     products_array = cart.products.all()
        #     # print(products_array)
        #     cart.total_cost = CalculateTotal(products_array)
        #     cart.save()

        #     # Return updated cart
        #     serialized_cart = PopulatedCartSerializer(cart)
        #     return Response(serialized_cart.data, status=status.HTTP_200_OK)

        # except Cart.DoesNotExist:
        #     return Response(
        #         {"detail": f"No cart found for user {request.user.username}"},
        #         status=status.HTTP_404_NOT_FOUND
            # )


class AddCartItemView(APIView):
    # Get or update the current user's cart
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:

            # Get users cart
            try:
                cart_user = Cart.objects.get(owner=request.user)
            except Cart.DoesNotExist:
                raise NotFound(
                    detail=f"Can't find Cart for user {request.user.username}")

            # Get data from the request
            quantity = request.data.get("quantity")
            product_id = request.data.get("product")

            if not product_id:
                return Response({"detail": "product_id is required"},status=status.HTTP_400_BAD_REQUEST)
            
            if not quantity:
                return Response({"detail": "quantity is required"},status=status.HTTP_400_BAD_REQUEST)
            
            if quantity <= 0:
                return Response({"detail": "quantity is required"},status=status.HTTP_400_BAD_REQUEST)

            try:
                product = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                raise NotFound(
                    detail=f"Can't find Product with id: {product_id}")

            cart_item_exists = CartItem.objects.filter(
                cart=cart_user, product=product).exists()

            if cart_item_exists:
                current_item = CartItem.objects.get(
                    cart=cart_user, product=product)
                current_item.quantity += quantity
                current_item.save()
            else:
                request.data["cart"] = cart_user.id
                cart_item_to_add = CartItemSerializer(data=request.data)
                print("cart_item_to_add:", cart_item_to_add)

                cart_item_to_add.is_valid(raise_exception=True)
                cart_item_to_add.save()

            cart_user.total_cost = CalculateTotal(cart_user.cart_items.all())

            cart_user.save()

              # Serialize the updated cart
            serialized_new_cart = PopulatedCartSerializer(cart_user)
            return Response(serialized_new_cart.data, status=status.HTTP_200_OK)
        except Exception as e:
                print("Error: ", {e})
                return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ClearCartView(APIView):
    # empty cart - d we need ?
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        try:
            cart = Cart.objects.get(owner=request.user)

            # Clear all products
            cart.products.clear()
            cart.total_cost = 0
            cart.save()

            # Return empty cart
            serialized_cart = PopulatedCartSerializer(cart)
            return Response(serialized_cart.data, status=status.HTTP_200_OK)

        except Cart.DoesNotExist:
            return Response(
                {"detail": f"No cart found for user {request.user.username}"},
                status=status.HTTP_404_NOT_FOUND
            )


def CalculateTotal(cart_items):
    sum = 0
    # print("products",products)
    if len(cart_items) > 0:
        for cart_item in cart_items:
            sum += cart_item.product.price * cart_item.quantity

        return sum
    else:
        return sum
