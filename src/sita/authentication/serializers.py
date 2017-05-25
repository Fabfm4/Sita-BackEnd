# -*- coding: utf-8 -*-

import hashlib
import random
from rest_framework import serializers
from sita.users.models import User
from sita.subscriptions.models import Subscription
from sita.utils.refresh_token import create_token
from hashlib import md5
from datetime import datetime, timedelta
import pytz

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
    device_os= serializers.ChoiceField(
        required=False,
        choices=['ANDROID', 'IOS']
    )
    device_token= serializers.CharField(
        required=False,
        max_length=254
    )

    def validate(self, data):
        """
        Validation email, password and active status
        """
        try:
            user = User.objects.get(email__exact=data.get('email'))
        except User.DoesNotExist:
            raise serializers.ValidationError({"email":"invalid credentials"})

        if not user.check_password(data.get('password')):
            raise serializers.ValidationError({"email":"invalid credentials"})

        if data.get("device_os") or data.get("device_token"):
            if not data.get("device_os") or not data.get("device_token"):
                raise serializers.ValidationError(
                    {"device_token":"Don`t send device OS or device token"})

        if not user.is_active:
            raise serializers.ValidationError(
                {"email":"The user is not actived"}
            )

        return data

    def get_user(self, data):
        """
        return user object
        """
        return User.objects.get(email__exact=data.get('email'))

class SignUpSerializer(serializers.Serializer):
    """"""
    TYPE_OS = (
        ('1', 'IOS'),
        ('2', 'ANDROID')
    )
    email = serializers.EmailField(
        max_length=254,
        required=True
    )
    password = serializers.CharField(
        max_length=100,
        required=True
    )
    time_zone = serializers.CharField(
        max_length=100,
        required=True
    )
    name = serializers.CharField(
        required=False,
        max_length = 100
    )
    phone = serializers.CharField(
        required=False,
        max_length=10
    )
    device_os= serializers.ChoiceField(
        required=False,
        choices=['ANDROID', 'IOS']
    )
    device_token= serializers.CharField(
        required=False,
        max_length=254
    )
    conekta_card = serializers.CharField(
        max_length=254,
        required=False
    )
    subscription_id= serializers.IntegerField(
        required=False
    )

    def validate(self, data):
        if data.get("device_os") or data.get("device_token"):
            if not data.get("device_os") or not data.get("device_token"):
                raise serializers.ValidationError(
                    {"device_token":"Don`t send device OS or device token"})

        if data.get("conekta_card"):
            if not data.get("phone") or not data.get("name") or not data.get("subscription_id"):
                raise serializers.ValidationError(
                    {"conekta_card":
                        "If send conektaCard you should send phone and name"})
            try:
                subscription = Subscription.objects.get(id=data.get('subscription_id'))
            except Subscription.DoesNotExist:
                raise serializers.ValidationError(
                    {"subscription_id":"That subscription don't exists"}
                    )

        try:
            user = User.objects.get(email__exact=data.get('email'))
            raise serializers.ValidationError(
                {"email":"The user is not actived"}
                )
        except User.DoesNotExist:
            pass
        try:
            datetime.now(pytz.timezone(data.get("time_zone")))
        except pytz.UnknownTimeZoneError:
            raise serializers.ValidationError(
                {"time_zone":"The time zone is not correct"}
                )

        return data

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
                {"email":"The user is not actived"}
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
            raise serializers.ValidationError(
                {"recovery_code":"Don't exits code"})

        if not data.get('password') == data.get('password_confim'):
            raise serializers.ValidationError(
                {"password_confim":
                "Password is not equals to Confirm Password"})

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
