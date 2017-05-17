from rest_framework import status, viewsets
from sita.core.api.mixins import base as base_mixins
from sita.api.v1.routers import router
from rest_framework.response import Response
from sita.core.api.routers.single import SingleObjectRouter
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    UserSerializerModel,
    UserSerializer,
    UserUpdatePasswordSerializer,
    UserPatchSerializer,
    UserListSerializer)
from .models import User
from rest_framework import serializers
from rest_framework_jwt.utils import jwt_get_user_id_from_payload_handler
from rest_framework_jwt.settings import api_settings
from sita.utils.refresh_token import has_permission
from django.core.urlresolvers import reverse
from rest_framework.decorators import detail_route
from django.contrib.auth import get_user_model
from sita.utils.urlresolvers import get_query_params
from rest_framework.decorators import detail_route


class UserViewSet(
    base_mixins.CreateModelMixin,
    viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    list_serializer_class = UserSerializerModel

    def create(self, request, *args, **kwards):
        """
        Create user by Admin.
        ---
        omit_serializer: true
        omit_parameters:
            - form
        parameters:
            - name: body
              type: UserSerializer
              paramType: body
              description:
                'email: <b>required</b> <br>
                password: <b>required</b> <br>
                name:NOT required <br>
                firstName: NOT required <br>
                mothersName: NOT required <br>
                phone: NOT required'
            - name: Authorization
              description: Bearer {token}.
              required: true
              type: string
              paramType: header
        responseMessages:
            - code: 201
              message: CREATED
            - code: 400
              message: BAD REQUEST
            - code: 500
              message: INTERNAL SERVER ERROR
        consumes:
            - application/json
        produces:
            - application/json
        """


        # Verify if the user has permission to use
        if has_permission(request.META):
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
                return Response(
                    headers={
                        "user":request.get_full_path() + "/{0}".format(user.id)
                        },
                    status=status.HTTP_201_CREATED)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @detail_route(methods=['PUT'])
    def update_password(self, request, pk=None):
        """
        User Create.
        ---
        omit_serializer: true
        omit_parameters:
            - form
        parameters:
            - name: body
              pytype: UserUpdatePasswordSerializer
              paramType: body
              description:
                'password: <b>required</b> <br>
                confirmPassword: <b>required</b>'
            - name: Authorization
              description: Bearer {token}.
              required: true
              type: string
              paramType: header
        responseMessages:
            - code: 400
              message: BAD REQUEST
            - code: 401
              message: UNAUTHORIZED
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
        serializer = UserUpdatePasswordSerializer(data=request.data)

        # Verify if exits the user with pk
        if User.objects.exists_user(pk=pk):
            user = User.objects.get(id=pk)
            # Verify if the user has permission to use
            if has_permission(request.META, user):
                serializer = UserUpdatePasswordSerializer(data=request.data)
                if serializer.is_valid():
                    user.set_password(request.data.get("password"))
                    user.save()
                    return Response(status=status.HTTP_200_OK)
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        """
        User login.
        ---
        omit_serializer: true
        omit_parameters:
            - form
        parameters:
            - name: body
              pytype: UserPatchSerializer
              paramType: body
              description:
                'name: NOT required <br>
                firstName: NOT required <br>
                mothersName: NOT required <br>
                phone: NOT required'
            - name: Authorization
              description: Bearer {token}.
              required: true
              type: string
              paramType: header
        responseMessages:
            - code: 200
              message: OK
            - code: 401
              message: UNAUTHORIZED
            - code: 404
              message: NOT_FOUND
            - code: 400
              message: BAD REQUEST
            - code: 500
              message: INTERNAL SERVER ERROR
        consumes:
            - application/json
        produces:
            - application/json
        """
        # Verify if exits the user with pk
        if User.objects.exists_user(pk=pk):
            user = User.objects.get(id=pk)
            # Verify if the user has permission to use
            if has_permission(request.META, user):
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
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)

            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):
        """
        View user with pk.
        ---
        response_serializer: UserSerializerModel
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
            - code: 401
              message: UNAUTHORIZED
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

        # Verify if exits the user with pk
        if User.objects.exists_user(pk=pk):
            user = User.objects.get(id=pk)
            # Verify if the user has permission to use
            if has_permission(request.META, user):
                    response_serializer = UserSerializerModel(user)
                    return Response({"data":response_serializer.data})

            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return Response(status=status.HTTP_404_NOT_FOUND)

class UserListViewSet(
    base_mixins.ListModelMixin,
    viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializerModel
    list_serializer_class = UserSerializerModel

    def get_queryset(self, *args, **kwargs):

        queryset = get_user_model().objects.all()
        query_params = get_query_params(self.request)
        q = query_params.get('q')

        if q:
            queryset = queryset.filter(email__contains=q)

        return queryset


    def list(self, request, *args, **kwargs):
        """
        Return a list of users, that matches with the given word.
        ---
        response_serializer: UserListSerializer
        parameters:
            - name: Authorization
              description: Bearer {token}.
              required: true
              type: string
              paramType: header
            - name: q
              description: Search word.
              paramType: query
              type: string
        responseMessages:
            - code: 200
              message: OK
            - code: 403
              message: FORBIDDEN
            - code: 500
              message: INTERNAL SERVER ERROR
        consumes:
            - application/json
        produces:
            - application/json
        """
        # Verify if the user has permission to use
        if has_permission(request.META):
            return super(UserListViewSet, self).list(request, *args, **kwargs)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


router.register(
    r'users',
    UserViewSet,
    base_name='user'
)
router.register(
    r'search/user',
    UserListViewSet,
    base_name='search/user'
)
