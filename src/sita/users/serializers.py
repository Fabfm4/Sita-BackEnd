from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model

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
    password = serializers.CharField(
        max_length=254,
        required=True
    )
    phone = serializers.CharField(
        max_length=10,
        required=False
    )

    def validate(self, data):
        try:
            user = User.objects.get(email__exact=data.get('email'))
            raise serializers.ValidationError(
                {"email": "The email is already exists"})
        except User.DoesNotExist:
            pass

        return data

class UserListSerializer(serializers.Serializer):
    """"""
    id = serializers.IntegerField(
        read_only=True
    )
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
    password = serializers.CharField(
        max_length=254,
        required=True
    )
    phone = serializers.CharField(
        max_length=10,
        required=False
    )

class SearchUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id',
                'name',
                'first_name',
                'mothers_name',
                'is_active',
                'email',
                'has_subscription',
                'is_superuser',
                'reset_pass_code',
                'phone', )

    def get_text(self, instance):
        return instance.email

class UserPatchSerializer(serializers.Serializer):
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
    phone = serializers.CharField(
        max_length=10,
        required=False
    )

class UserUpdatePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=254,
        required=True
    )
    confirm_password = serializers.CharField(
        max_length=254,
        required=True
    )
    def validate(self, data):
        if data.get("confirm_password") != data.get("password"):
            raise serializers.ValidationError(
                "The passwords are not equals"
            )

        return data

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
                'reset_pass_code',
                'phone', )
