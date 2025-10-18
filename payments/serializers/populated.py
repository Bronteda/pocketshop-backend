from payments.serializers.common import PaymentSerializer
from jwt_auth.serializers import UserSerializer


class PopulatedPaymentSerializer(PaymentSerializer):
    owner = UserSerializer()
