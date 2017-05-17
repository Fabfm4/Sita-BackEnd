from rest_framework import serializers
from .models import Patient
from sita.users.models import User

class PatientSerializer(serializers.Serializer):
    """"""
    name = serializers.CharField(
        required = True,
        max_length = 100
    )
    last_name = serializers.CharField(
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
    age = serializers.IntegerField(
        required = False
    )
    mobile_phone = serializers.CharField(
        required = True,
        max_length=10
    )
    house_phone = serializers.CharField(
        max_length=10,
        required = False
    )

class PatientSerializerModel(serializers.ModelSerializer):
    """
    Serializer used to return the proper token, when the user was succesfully
    logged in.
    """

    class Meta:
        model = Patient
        fields = ('id',
                'name',
                'last_name',
                'mothers_name',
                'email',
                'age',
                'mobile_phone',
                'house_phone',
                'user' )
