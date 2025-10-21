
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
    
    #We would be in cart view which has the URL with the pk
    def delete(self, request):
        try:
            # Get users cart
            try:
                cart_user = Cart.objects.get(owner=request.user)
            except Cart.DoesNotExist:
                raise NotFound(
                    detail=f"Can't find Cart for user {request.user.username}")

            #get product_id from request
            product_id = request.data.get("product")
            if not product_id:
                return Response({"detail": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST)

            #find the cart item
            cart_item = CartItem.objects.get(cart = cart_user,product=product_id)

            #Delete item from cart
            cart_item.delete()

            #recalculate the total
            cart_user.total_cost = CalculateTotal(cart_user.cart_items.all())

            cart_user.save()
            #serialize cart
            serialized_new_cart = PopulatedCartSerializer(cart_user)

            return Response(serialized_new_cart.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("Error: ", {e})
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
    #update quantity 
    def patch(self, request):
        try:
         # Get users cart
            try:
                cart_user = Cart.objects.get(owner=request.user)
            except Cart.DoesNotExist:
                raise NotFound(
                    detail=f"Can't find Cart for user {request.user.username}")
            
            #get product_id from request
            product = request.data.get("product")
            if not product:
                return Response({"detail": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            #get quantity from request
            quantity = request.data.get("quantity")
            #We use is None because if you say 0 it take it as falsy and will hit this endpoint if quantity is 0
            if quantity is None:
                return Response({"detail": "quantity is required"}, status=status.HTTP_400_BAD_REQUEST)
            #checking quantity is an integer
            try:
                quantity = int(quantity)
            except (ValueError, TypeError):
                return Response({"detail": "quantity must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)
            
            #Check if quantity not negative
            if quantity < 0:
                return Response({"detail": "quantity is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            #find the cart item
            try:
                cart_item = CartItem.objects.get(cart = cart_user,product=product)
            except Exception as e:
                return Response({"detail":"Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

            #if quantity given is 0 delete product item
            if int(quantity) == 0 :
                #Delete item from cart
                cart_item.delete()
            else:
                cart_item.quantity = quantity
                cart_item.save()

            #Recalculate
            cart_user.total_cost=CalculateTotal(cart_user.cart_items.all())

            #Save cart
            cart_user.save()

            serialized_saved_cart = PopulatedCartSerializer(cart_user)
            return Response(serialized_saved_cart.data, status=status.HTTP_200_OK)

        except Exception as e:
            print("Error: ", {e})
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)


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
            product = request.data.get("product")

            if not product:
                return Response({"detail": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST)

            if not quantity:
                return Response({"detail": "quantity is required"}, status=status.HTTP_400_BAD_REQUEST)

            if quantity <= 0:
                return Response({"detail": "quantity is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                product = Product.objects.get(pk=product)
            except Product.DoesNotExist:
                raise NotFound(
                    detail=f"Can't find Product with id: {product}")
            
            #seeing if that cart item exists 
            cart_item_exists = CartItem.objects.filter(
                cart=cart_user, product=product).exists()

            #if that cart item exists increase the quantity else create new
            if cart_item_exists:
                #Getting the current work item
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

            #recalculate total
            cart_user.total_cost = CalculateTotal(cart_user.cart_items.all())

            #Save cart
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
