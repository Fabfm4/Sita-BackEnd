# -*- coding: utf-8 -*-
from rest_framework import status, viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from pprint import pprint

from sita.api.v1.routers import router
from sita.authentication import serializers
from sita.core.api.routers.single import SingleObjectRouter

import sys

class LoginViewSet(viewsets.GenericViewSet):
    permission_classes = (AllowAny, )

    serializer_class = serializers.LoginSerializer

    @detail_route(methods=['POST'])
    def login(self, request, *args, **kwards):
        """
        User login.
        ---
        omit_parameters:
            - form
        parameters:
            - name: body
              type: LoginSerializer
              paramType: body
        responseMessages:
            - code: 400
              message: BAD REQUEST
            - code: 200
              message: OK
            - code: 500
              message: INTERNAL SERVER ERROR
        consumes:
            - application/json
        produces:
            - application/json
        """

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            user = serializer.get_user(serializer.data)
            response_serializer = serializers.LoginResponseSerializer()
            return Response(response_serializer.get_token(user))


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecoveryPasswordViewSet(viewsets.GenericViewSet):
    permission_classes = (AllowAny, )

    serializer_class = serializers.RecoveryPasswordSerializer

    @detail_route(methods=['POST'])
    def recovery_password(self, request, *args, **kwards):
        """
        Recovery Password.
        ---
        omit_parameters:
            - form
        parameters:
            - name: body
              type: RecoveryPasswordSerializer
              paramType: body
        responseMessages:
            - code: 400
              message: BAD REQUEST
            - code: 200
              message: OK
            - code: 500
              message: INTERNAL SERVER ERROR
        consumes:
            - application/json
        produces:
            - application/json
        """

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.generate_recovery_token(serializer.data)
            return Response()

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordWithCodeViewSet(viewsets.GenericViewSet):

    permission_classes = (AllowAny, )
    serializer_class = serializers.ResetPasswordWithCodeSerializer

    @detail_route(methods=['POST'])
    def reset_password_code(self, request, *args, **kwards):
        """
        Reset Password.
        ---
        omit_parameters:
            - form
        parameters:
            - name: body
              type: ResetPasswordWithCodeSerializer
              paramType: body
        responseMessages:
            - code: 400
              message: BAD REQUEST
            - code: 200
              message: OK
            - code: 500
              message: INTERNAL SERVER ERROR
        consumes:
            - application/json
        produces:
            - application/json
        """

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.update_password(data=request.data)
            return Response()

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



router.register(
    r'auth',
    LoginViewSet,
    base_name="login",
    router_class=SingleObjectRouter
)
router.register(
    r'auth',
    RecoveryPasswordViewSet,
    base_name="recovery-password",
    router_class=SingleObjectRouter
)
router.register(
    r'auth',
    ResetPasswordWithCodeViewSet,
    base_name="reset-password-code",
    router_class=SingleObjectRouter
)
