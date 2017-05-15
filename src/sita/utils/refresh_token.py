# -*- coding: utf-8 -*-
from calendar import timegm
from datetime import datetime
from sita.users.serializers import UserSerializerModel

from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication


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
        'user': UserSerializerModel(user).data
    }

def get_user_by_token(meta):
    """Get user by Authenticate Token"""
    jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
    jwt_payload_get_user_id_handler = api_settings.JWT_PAYLOAD_GET_USER_ID_HANDLER
    user = jwt_decode_handler(meta.get("HTTP_AUTHORIZATION").replace("Bearer ", ""))
    return jwt_payload_get_user_id_handler(user)
