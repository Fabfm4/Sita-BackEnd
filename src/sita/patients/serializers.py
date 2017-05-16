from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.Serializer):
    """"""
    name = serializers.CharField(
        required = False,
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
    age = serializers.IntegerField()
    mobile_phone = serializers.CharField(
        max_length=10
    )
    house_phone = serializers.CharField(
        max_length=10
    )
