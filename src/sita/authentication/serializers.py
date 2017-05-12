# -*- coding: utf-8 -*-

import hashlib
import random
from rest_framework import serializers
from sita.users.models import User
from sita.utils.refresh_token import create_token
from hashlib import md5

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """

    email = serializers.EmailField(
        required=True
    )

    password = serializers.CharField(
        required=True
    )

    def validate(self, data):
        """
        Validation email, password and active status
        """
        try:
            user = User.objects.get(email__exact=data.get('email'))
        except User.DoesNotExist:
            raise serializers.ValidationError("invalid credentials")

        if not user.check_password(data.get('password')):
            raise serializers.ValidationError("invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError(
                "The user has not been actived"
            )

        return data

    def get_user(self, data):
        """
        return user object
        """
        return User.objects.get(email__exact=data.get('email'))

class LoginResponseSerializer(serializers.ModelSerializer):
    """
    Serializer used to return the proper token, when the user was succesfully
    logged in.
    """
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('token', )

    def get_token(self, obj):
        """
        Create token.
        """
        return create_token(obj)

class RecoveryPasswordSerializer(serializers.Serializer):
    """
    Serializer for user recovery password
    """

    email = serializers.EmailField(
        required=True
    )

    def validate(self, data):
        """
        Validation email and active status
        """
        try:
            user = User.objects.get(email__exact=data.get('email'))
        except User.DoesNotExist:
            raise serializers.ValidationError("invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError(
                "The user has not been actived"
            )

        return data

    def generate_recovery_token(self, data):
        """ Generate code to recovery password. """

        user = User.objects.get(email__exact=data.get('email'))
        email = user.email
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        if isinstance(email, unicode):
            email = email.encode('utf-8')

        key = hashlib.sha1(salt + email).hexdigest()
        user.reset_pass_code = key
        user.save()
        return True
