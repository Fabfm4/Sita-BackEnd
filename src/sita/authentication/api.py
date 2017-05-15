# -*- coding: utf-8 -*-
from rest_framework import status, viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from sita.api.v1.routers import router
from sita.users.models import User, Device
from sita.authentication import serializers
from sita.core.api.routers.single import SingleObjectRouter

class LoginViewSet(viewsets.GenericViewSet):
    permission_classes = (AllowAny, )

    serializer_class = serializers.LoginSerializer

    @detail_route(methods=['POST'])
    def signin(self, request, *args, **kwards):
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
            device_token=request.data.get("device_token")
            device_os=request.data.get("device_os")
            if device_token and device_os:
                device = Device.objects.register(
                    device_token=device_token,
                    device_os=device_os,
                    user=user)
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

class SignUpViewSet(viewsets.GenericViewSet):
    permission_classes = (AllowAny, )
    serializer_class = serializers.SignUpSerializer

    @detail_route(methods=['POST'])
    def signup(self, request, *args, **kwards):
        """
        User login.
        ---
        omit_parameters:
            - form
        parameters:
            - name: body
              type: SignUpSerializer
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
            for key in request.data:
                if key == "name" or key == "phone" or key == "conekta_card":
                    kwards.setdefault(key,request.data.get(key))
            user = User.objects.create_user(
                email=request.data.get("email"),
                password=request.data.get("password"),
                **kwards
            )

            device_token=request.data.get("device_token")
            device_os=request.data.get("device_os")
            if device_token and device_os:
                device = Device.objects.register(
                    device_token=device_token,
                    device_os=device_os,
                    user=user)

            response_serializer = serializers.LoginResponseSerializer()
            return Response(response_serializer.get_token(user))


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


router.register(
    r'auth',
    LoginViewSet,
    base_name="signin",
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
router.register(
    r'auth',
    SignUpViewSet,
    base_name="signup",
    router_class=SingleObjectRouter
)
