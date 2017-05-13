from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
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
