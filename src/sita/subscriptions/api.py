from rest_framework import status, viewsets
from sita.core.api.mixins import base as base_mixins
from sita.api.v1.routers import router
from rest_framework.response import Response
from sita.core.api.routers.single import SingleObjectRouter
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import (
    SubscriptionSerializer,
    SubscriptionSerializerModel)
from rest_framework import serializers
from rest_framework_jwt.utils import jwt_get_user_id_from_payload_handler
from rest_framework_jwt.settings import api_settings
from sita.utils.refresh_token import has_permission
from django.core.urlresolvers import reverse
from rest_framework.decorators import detail_route
from django.contrib.auth import get_user_model
from sita.utils.urlresolvers import get_query_params
from rest_framework.decorators import detail_route
from .models import Subscription


class SubscriptionViewSet(
    # base_mixins.CreateModelMixin,
    base_mixins.ListModelMixin,
    base_mixins.RetrieveModelMixin,
    base_mixins.PartialUpdateModelMixin,
    viewsets.GenericViewSet):
    serializer_class =  SubscriptionSerializerModel
    retrieve_serializer_class = SubscriptionSerializerModel
    partial_update_serializer_class = SubscriptionSerializerModel
    update_serializer_class = SubscriptionSerializerModel
    permission_classes = (IsAuthenticated, AllowAny, )

    def get_queryset(self, *args, **kwargs):

        queryset = Subscription.objects.all()
        query_params = get_query_params(self.request)
        q = query_params.get('q')

        if q:
            queryset = queryset.filter(name__icontains=q)

        return queryset

    def list(self, request, *args, **kwards):
        """
        List all patitent from user with filter
        ---
        omit_parameters:
            - form
        parameters:
            - name: Authorization
              description: Bearer {token}.
              required: false
              type: string
              paramType: header
            - name: q
              description: Search word.
              paramType: query
              type: string
        responseMessages:
            - code: 200
              message: OK
            - code: 400
              message: BAD REQUEST
            - code: 500
              message: INTERNAL SERVER ERROR
        consumes:
            - application/json
        produces:
            - application/json
        """
        return super(
            SubscriptionViewSet, self).list(
                request,
                queryset=self.get_queryset(),
                *args,
                **kwards)

    def create(self, request, *args, **kwards):
        """
        Create patient from user
        ---
        omit_parameters:
            - form
        parameters:
            - name: body
              pytype: SubscriptionSerializer
              paramType: body
              description:
                'title: <b>required</b> <br>
                timeInMinutes: <b>required</b> <br>
                description: <b>required</b>'
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

        if has_permission(request.META):
            serializer = SubscriptionSerializer(data=request.data)
            if serializer.is_valid():
                fields = Subscription().get_fields()
                Subscription.objects.register(
                    data=request.data, fields=fields)
                return Response(status=status.HTTP_201_CREATED)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, pk=None,  *args, **kwards):
        """
        View a specific patient
        ---
        omit_parameters:
            - form
        parameters:
            - name: Authorization
              description: Bearer {token}.
              required: false
              type: string
              paramType: header
        responseMessages:
            - code: 200
              message: OK
            - code: 500
              message: INTERNAL SERVER ERROR
        consumes:
            - application/json
        produces:
            - application/json
        """
        if Subscription.objects.exists(pk=pk):
            subscription = Subscription.objects.get(pk=pk)
            return super(
                SubscriptionViewSet, self).retrieve(
                    request,
                    pk=pk,
                    *args,
                    **kwards)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        """
        Update information from an specific patient
        ---
        omit_parameters:
            - form
        parameters:
            - name: body
              pytype: SubscriptionSerializer
              paramType: body
              description:
                'title: NOT required <br>
                timeInMinutes: NOT required <br>
                description: NOT required'
            - name: Authorization
              description: Bearer {token}.
              required: true
              type: string
              paramType: header
        responseMessages:
            - code: 200
              message: OK
            - code: 400
              message: BAD REQUEST
            - code: 500
              message: INTERNAL SERVER ERROR
        consumes:
            - application/json
        produces:
            - application/json
        """
        if Subscription.objects.exists(pk=pk):
            subscription = Subscription.objects.get(pk=pk)
            if has_permission(request.META):
                return super(SubscriptionViewSet, self).partial_update(request, pk)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """
        Write the status from patient
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
            - code: 500
              message: INTERNAL SERVER ERROR
        consumes:
            - application/json
        produces:
            - application/json
        """
        if Subscription.objects.exists(pk=pk):
            subscription = Subscription.objects.get(pk=pk)
            if has_permission(request.META):
                subscription.delete()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_404_NOT_FOUND)

router.register(
    r'subscriptions',
    SubscriptionViewSet,
    base_name='subscriptions'
)
