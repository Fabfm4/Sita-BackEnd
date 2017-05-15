from rest_framework import serializers
from .models import User

class UserSerializer(serializers.Serializer):
    """"""
    name = serializers.CharField(
        required = False,
        max_length = 100
    )
    first_name = serializers.CharField(
        max_length=100,
        required=False
    )
    mothers_name = serializers.CharField(
        max_length=100,
        required=False
    )
    email = serializers.EmailField(
        max_length=254,
        required=True
    )
    conekta_customer = serializers.CharField(
        max_length=254,
        required=False
    )
    phone = serializers.CharField(
        max_length=10,
        required=False
    )



class UserSerializerModel(serializers.ModelSerializer):
    """
    Serializer used to return the proper token, when the user was succesfully
    logged in.
    """

    class Meta:
        model = User
        fields = ('id',
                'name',
                'first_name',
                'mothers_name',
                'is_active',
                'email',
                'has_subscription',
                'is_superuser',
                'reset_pass_code', )
