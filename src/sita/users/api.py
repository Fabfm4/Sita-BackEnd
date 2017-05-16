from rest_framework import status, viewsets
from sita.core.api.mixins import base as base_mixins
from sita.api.v1.routers import router
from rest_framework.response import Response
from sita.core.api.routers.single import SingleObjectRouter
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    UserSerializerModel, UserSerializer, UserUpdatePasswordSerializer, UserPatchSerializer)
from .models import User
from rest_framework import serializers
from rest_framework_jwt.utils import jwt_get_user_id_from_payload_handler
from rest_framework_jwt.settings import api_settings
from sita.utils.refresh_token import get_user_by_token
from django.core.urlresolvers import reverse
from rest_framework.decorators import detail_route


class UserViewSet(
    base_mixins.CreateModelMixin,
    base_mixins.UpdateModelMixin,
    viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer

    def create(self, request, *args, **kwards):
        """
        User login.
        ---
        type:
          pk:
            required: true
            type: string
          Authorization:
            required: true
            type: string
        omit_parameters:
            - form
        parameters:
            - name: body
              type: UserSerializer
              paramType: body
            - name: Authorization
              description: Bearer {token}.
              required: true
              type: string
              paramType: header
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

        usernameToken = User.objects.get(id=get_user_by_token(request.META))
        if usernameToken.is_superuser:
            if serializer.is_valid():
                for key in request.data:
                    if key == "name" or key == "phone" or key == "conekta_card":
                        kwards.setdefault(key,request.data.get(key))
                user = User.objects.create_user(
                    email=request.data.get("email"),
                    password=request.data.get("password"),
                    **kwards
                )
                return Response(headers={"user":request.get_full_path() + "/{0}".format(user.id)},
                    status=status.HTTP_201_CREATED)


            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @detail_route(methods=['PUT'])
    def update_password(self, request, pk=None):
        """
        User Create.
        ---
        type:
          pk:
            required: true
            type: string
          Authorization:
            required: true
            type: string
        serializer: UserUpdatePasswordSerializer
        omit_parameters:
            - form
        parameters:
            - name: body
              pytype: UserUpdatePasswordSerializer
              paramType: body
            - name: Authorization
              description: Bearer {token}.
              required: true
              type: string
              paramType: header
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
        serializer = UserUpdatePasswordSerializer(data=request.data)
        usernameToken = User.objects.get(id=get_user_by_token(request.META))
        if serializer.is_valid():
            try:
                user = User.objects.get(id=pk)
                if user.email == usernameToken.email or usernameToken.is_superuser:
                    user.set_password(request.data.get("password"))
                    user.save()
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"message": "Unauthorized"},
                        status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response(
                    {"message": "Not Found"},
                    status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """
        User login.
        ---
        type:
          pk:
            required: true
            type: string
          Authorization:
            required: true
            type: string
        omit_parameters:
            - form
        parameters:
            - name: body
              type: UserSerializer
              paramType: body
            - name: Authorization
              description: Bearer {token}.
              required: true
              type: string
              paramType: header
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
        try:
            user = User.objects.get(id=pk)
            usernameToken = User.objects.get(id=get_user_by_token(request.META))
            if user.email == usernameToken.email or usernameToken.is_superuser:
                serializer = UserPatchSerializer(data=request.data)
                if serializer.is_valid():
                    for key in request.data:
                        if key == "name":
                            user.name = request.data.get(key)
                        if key == "first_name":
                            user.first_name = request.data.get(key)
                        if key == "mothers_name":
                            user.mothers_name = request.data.get(key)
                        if key == "phone":
                            user.phone = request.data.get(key)
                        user.save()
                        return Response(
                            status=status.HTTP_200_OK)
                else:
                    return Response(
                        serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    {"message": "Unauthorized"},
                    status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response(
                {"message": "Not Found"},
                status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):
        """
        User Create.
        ---
        type:
          pk:
            required: true
            type: string
          Authorization:
            required: true
            type: string
        omit_serializer: false
        parameters:
            - name: pk
              description: Photo user.
              required: true
              type: integer
              paramType: path
            - name: Authorization
              description: Bearer {token}.
              required: true
              type: string
              paramType: header
        responseMessages:
            - code: 400
              message: BAD REQUEST
            - code: 404
              message: NOT FOUND
            - code: 200
              message: OK
            - code: 500
              message: INTERNAL SERVER ERROR
        consumes:
            - application/json
        produces:
            - application/json
        """
        try:
            user = User.objects.get(id=pk)
            usernameToken = User.objects.get(id=get_user_by_token(request.META))
            if user.email == usernameToken.email or usernameToken.is_superuser:
                response_serializer = UserSerializerModel(user)
            else:
                return Response(
                    {"message": "user not found"},
                    status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response(
                {"message": "user not found"},
                status=status.HTTP_404_NOT_FOUND)

        return Response({"data":response_serializer.data})

    def list(self, request):
        """
        User Create.
        ---
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
        pass
        # usernameToken = User.objects.get(id=get_user_by_token(request.META))
        # if usernameToken.is_superuser:

router.register(
    r'user',
    UserViewSet,
    base_name='user'
)
