from rest_framework import serializers
from .models import Card
from sita.users.models import User

class CardSerializer(serializers.Serializer):
    """"""

    conekta_card = serializers.CharField(
        max_length=100,
        required=True
    )

class CardSerializerModel(serializers.ModelSerializer):
    """
    Serializer used to return the proper token, when the user was succesfully
    logged in.
    """

    class Meta:
        model = Card
        fields = ('id',
                'last_four',
                'brand_card',
                'conekta_card',
                'is_default',
                'user' )
