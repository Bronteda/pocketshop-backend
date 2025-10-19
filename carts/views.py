
from .serializers.common import CartSerializer
from .serializers.populated import PopulatedCartSerializer
from carts.models import Cart
from products.models import Product
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound


# Cart is created automatically when user registers (via signals.py)

class MyCartView(APIView):
    #Get or update the current user's cart
    permission_classes = [IsAuthenticated]

    #Get Auth users cart
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

    #add product to cart 
    #When you add a product you send in Product id and quantity
    def post(self, request):
        try:
            # Find the user's cart
            cart = Cart.objects.get(owner=request.user)
            # Add product to cart (assuming product ID is sent in request.data)
            product_id = request.data.get("product")
            if not product_id:
                return Response({"detail": "Product ID required."}, status=status.HTTP_400_BAD_REQUEST)
            #Add product to cart 
            cart.products.add(product_id)

            # #This is removing the quantity you are adding to your cart 
            # quantity_of_product = request.data.get("quantity")
            # find_product = Product.objects.get(pk=product_id)
            # print("found product:", find_product)
            # find_product.quantity - quantity_of_product
            # Product.save()

            products_array = cart.products.all() #work out all products in cart
            #print(products_array)
            cart.total_cost = CalculateTotal(products_array)

            cart.save()
            # Serialize the updated cart
            serialized_cart = PopulatedCartSerializer(cart)
            return Response(serialized_cart.data, status=status.HTTP_200_OK)
            
        except Cart.DoesNotExist:
            raise NotFound(
                detail=f"Can't find Cart for user {request.user.username}")



    #Remove product from cart
    def delete(self, request):
        try:
            cart = Cart.objects.get(owner=request.user)
            
            product_id = request.data.get("product")
            # Remove product from cart
            cart.products.remove(product_id)
            products_array = cart.products.all() #work out all products in cart after action
            #print(products_array)
            cart.total_cost = CalculateTotal(products_array)
            cart.save()
            
            # Return updated cart
            serialized_cart = PopulatedCartSerializer(cart)
            return Response(serialized_cart.data, status=status.HTTP_200_OK)
            
        except Cart.DoesNotExist:
            return Response(
                {"detail": f"No cart found for user {request.user.username}"},
                status=status.HTTP_404_NOT_FOUND
            )


class ClearCartView(APIView):
    #empty cart - d we need ? 
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



def CalculateTotal(products):
    sum = 0
    #print("products",products)
    if len(products)>0:
        for product in products:
            sum += product.price * product.quantity
        
        return sum
    else:
        return sum

