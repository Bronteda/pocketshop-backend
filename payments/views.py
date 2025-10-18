
# pylint: disable=no-member
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers.common import PaymentSerializer
from .serializers.populated import PopulatedPaymentSerializer
from .models import Payment


# This returns all payments in DB (mostly used for testing)
class PaymentListView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, _request):
        try:
            payments = Payment.objects.all()

            if not payments.exists():
                return Response({"message": "No payments found in db"}, status=status.HTTP_404_NOT_FOUND)

            serialized_payments = PopulatedPaymentSerializer(
                payments, many=True)
            return Response(serialized_payments.data, status=status.HTTP_200_OK)

        except Exception as e:
            print("Error: ", {e})
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    # Body req is not required due to defaults
    def post(self, request):
        # expiration_date needs to come back from request.data
        # ^ we don't add this to payment, but we VALIDATE that the date is correct (utilize mock service)
        # if correct, we create payment and mark as SUCCESS ?

        request.data["owner"] = request.user.id
        payment_to_add = PaymentSerializer(data=request.data)
        print("payment_to_add:", payment_to_add)

        try:
            payment_to_add.is_valid(raise_exception=True)
            payment_to_add.save()
            return Response(payment_to_add.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error: ", {e})
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)


# GET, PUT, DELETE a Payment
class PaymentDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_payment(self, pk):
        try:
            return Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            raise NotFound("🆘 Can't find that Payment")

    # GET/SHOW Payment
    def get(self, _request, pk):
        payment = self.get_payment(pk=pk)
        serialized_payment = PopulatedPaymentSerializer(payment)
        return Response(serialized_payment.data, status=status.HTTP_200_OK)

    # PUT/UPDATE Payment -- NOT SURE IF THIS IS NEEDED ?
    def put(self, request, pk):
        payment_to_update = self.get_payment(pk=pk)
        print("payment_to_update:", payment_to_update)
        request.data['owner'] = request.user.id

        updated_payment = PaymentSerializer(
            payment_to_update, data=request.data)

        if updated_payment.is_valid():
            updated_payment.save()
            return Response(updated_payment.data, status=status.HTTP_202_ACCEPTED)

        return Response(updated_payment.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    # DELETE Payment
    def delete(self, request, pk):
        payment_to_delete = self.get_payment(pk)
        payment_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
