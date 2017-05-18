from rest_framework import serializers
from .models import Card
from sita.users.models import User

class CardSerializer(serializers.Serializer):
    """"""
    last_four = serializers.CharField(
        required = True,
        max_length = 100
    )
    type_card = serializers.CharField(
        max_length=100,
        required=True
    )
    conekta_card = serializers.CharField(
        max_length=100,
        required=True
    )
    is_default = serializers.EmailField(
        max_length=254,
        required=False
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
                'type_card',
                'conekta_card',
                'is_default',
                'user' )
