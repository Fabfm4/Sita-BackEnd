from rest_framework import status, viewsets
from sita.core.api.mixins import base as base_mixins
from sita.api.v1.routers import router
from rest_framework.response import Response
from sita.core.api.routers.single import SingleObjectRouter
from rest_framework.permissions import AllowAny

class UserViewSet(
    base_mixins.CreateModelMixin,
    base_mixins.UpdateModelMixin,
    viewsets.GenericViewSet):
    permission_classes = (AllowAny, )

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
        return Response(True)


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

router.register(
    r'user',
    UserViewSet,
    base_name='user'
)
