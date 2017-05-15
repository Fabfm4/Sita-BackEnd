from rest_framework import status, viewsets
from sita.core.api.mixins import base as base_mixins
from sita.api.v1.routers import router
from rest_framework.response import Response
from sita.core.api.routers.single import SingleObjectRouter
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializerModel
from .models import User
from rest_framework import serializers
from rest_framework_jwt.utils import jwt_get_user_id_from_payload_handler
from rest_framework_jwt.settings import api_settings
from sita.utils.refresh_token import get_user_by_token


class UserViewSet(
    base_mixins.CreateModelMixin,
    base_mixins.UpdateModelMixin,
    viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    def create(self, request):
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


    def update(self, request, pk=None):
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

    def partial_update(self, request, pk=None):
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
