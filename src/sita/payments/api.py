from sita.core.api.viewsets import GenericViewSet
from rest_framework import status
from sita.api.v1.routers import router
from sita.core.api.viewsets.nested import NestedViewset
from rest_framework.permissions import IsAuthenticated
from .serializers import PaymentSerializer, PaymentSerializerModel
from sita.users.api import UserViewSet
from sita.payments.models import Payment
from sita.users.models import User
from rest_framework.response import Response
from sita.utils.refresh_token import has_permission
from sita.core.api.mixins import base as base_mixins
from django.contrib.auth import get_user_model
from sita.utils.urlresolvers import get_query_params
from rest_framework.decorators import detail_route


class PaymentUserViewSet(
    base_mixins.ListModelMixin,
    GenericViewSet):
    serializer_class =  PaymentSerializerModel
    retrieve_serializer_class = PaymentSerializerModel
    partial_update_serializer_class = PaymentSerializerModel
    update_serializer_class = PaymentSerializerModel
    create_serializer_class = PaymentSerializerModel
    permission_classes = (IsAuthenticated, )

    def get_queryset(self, user_id=None, *args, **kwargs):

        queryset = Payment.objects.all()
        if user_id is not None:
            queryset = Payment.objects.filter(user_id=user_id)
        query_params = get_query_params(self.request)

        return queryset


    def list(self, request, user_pk=None, *args, **kwards):
        """
        Show all cards from user
        ---
        omit_parameters:
            - form
        parameters:
            - name: Authorization
              description: Bearer {token}.
              required: true
              type: string
              paramType: header
        responseMessages:
            - code: 200
              message: OK
            - code: 404
              message: NOT FOUND
            - code: 401
              message: UNAUTHORIZED
            - code: 500
              message: INTERNAL SERVER ERROR
        consumes:
            - application/json
        produces:
            - application/json
        """
        if User.objects.exists_user(pk=user_pk):
            user = User.objects.get(id=user_pk)
            if has_permission(request.META, user):
                return super(
                    PaymentUserViewSet, self).list(
                        request,
                        queryset=self.get_queryset(user.id),
                        *args,
                        **kwards    )
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_404_NOT_FOUND)


router.register_nested(
    r'users',
    r'payments',
    PaymentUserViewSet,
    parent_lookup_name='user',
    base_name='payments'
)
