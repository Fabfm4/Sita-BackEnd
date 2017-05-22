from rest_framework import serializers
from .models import Payment
from sita.users.models import User

class PaymentSerializer(serializers.Serializer):
    """"""
    conekta_id = serializers.CharField()
    card_last_four = serializers.CharField(
        max_length=4
    )
    card_brand = serializers.CharField(
        max_length=10
    )
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    description = serializers.CharField()
    reference_id_conekta = serializers.CharField()
    currency = serializers.CharField(
        max_length=10
    )
    title_subscription = serializers.CharField(
        max_length=254
    )
    user = serializers.IntegerField(
        required = True,
    )


class PaymentSerializerModel(serializers.ModelSerializer):
    """
    Serializer used to return the proper token, when the user was succesfully
    logged in.
    """

    class Meta:
        model = Payment
        fields = ('id',
                'conekta_id',
                'card_last_four',
                'amount' ,
                'card_brand',
                'description',
                'reference_id_conekta' ,
                'currency' ,
                'title_subscription' ,
                'created_date',
                'user' )
