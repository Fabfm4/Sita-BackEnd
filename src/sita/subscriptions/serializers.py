from rest_framework import serializers
from .models import Subscription

class SubscriptionSerializer(serializers.Serializer):
    """"""
    title = serializers.CharField(
        required = True,
        max_length = 100
    )
    time_in_minutes = serializers.CharField(
        max_length=100,
        required=True
    )
    description = serializers.CharField(
        max_length=100,
        required=True
    )
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

class SubscriptionSerializerModel(serializers.ModelSerializer):
    """
    Serializer used to return the proper token, when the user was succesfully
    logged in.
    """

    class Meta:
        model = Subscription
        fields = ('id',
                'title',
                'time_in_minutes',
                'description',
                'amount',)
