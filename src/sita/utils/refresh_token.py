# -*- coding: utf-8 -*-
from calendar import timegm
from datetime import datetime
from sita.users.serializers import UserSerializer

from rest_framework_jwt.settings import api_settings


def create_token(user):
    """
    Create token.
    """
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    # Return values
    data = jwt_encode_handler(payload)
    return jwt_response_payload_handler(data, user)

def jwt_response_payload_handler(token, user=None, request=None):
    """Response custom from rest_framework_jwt"""
    return {
        'token': token,
        'user': UserSerializer(user).data
    }
