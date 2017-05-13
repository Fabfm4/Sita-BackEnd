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

class LoginResponseSerializer(object):
    """
    Serializer used to return the proper token, when the user was succesfully
    logged in.
    """

    def __init__(self):
        pass

    def get_token(self,obj):
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

class ResetPasswordWithCodeSerializer(serializers.Serializer):
    """
    Serializer for user login
    """

    password = serializers.CharField(
        required=True
    )

    password_confim = serializers.CharField(
        required=True
    )

    recovery_code = serializers.CharField(
        required=True
    )

    def validate(self, data):
        """
        Validation email, password and active status
        """
        try:
            user = User.objects.get(reset_pass_code=data.get('recovery_code'))
        except User.DoesNotExist:
            raise serializers.ValidationError("Don't exits code")

        if not data.get('password') == data.get('password_confim'):
            raise serializers.ValidationError(
                "Password is not equals to Confirm Password")

        return data

    def update_password(self, data):
        """
        Change password
        """
        user = User.objects.get(reset_pass_code=data.get('recovery_code'))
        user.reset_pass_code = None
        user.set_password(data.get('password'))
        user.save()
        return True
