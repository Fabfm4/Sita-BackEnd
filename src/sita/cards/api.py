from sita.core.api.viewsets import GenericViewSet
from rest_framework import status
from sita.api.v1.routers import router
from sita.core.api.viewsets.nested import NestedViewset
from rest_framework.permissions import IsAuthenticated
from .serializers import CardSerializer, CardSerializerModel
from sita.users.api import UserViewSet
from sita.cards.models import Card
from sita.users.models import User
from rest_framework.response import Response
from sita.utils.refresh_token import has_permission
from sita.core.api.mixins import base as base_mixins
from django.contrib.auth import get_user_model
from sita.utils.urlresolvers import get_query_params
from sita.utils import conekta_sita
from rest_framework.decorators import detail_route

class CardUserViewSet(
    base_mixins.ListModelMixin,
    GenericViewSet):
    serializer_class =  CardSerializerModel
    retrieve_serializer_class = CardSerializerModel
    partial_update_serializer_class = CardSerializerModel
    update_serializer_class = CardSerializerModel
    create_serializer_class = CardSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self, user_id=None, *args, **kwargs):

        queryset = Card.objects.all()
        if user_id is not None:
            queryset = Card.objects.filter(user_id=user_id)
        query_params = get_query_params(self.request)
        q = query_params.get('q')

        if q:
            queryset = queryset.filter(name__icontains=q)

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
            - name: q
              description: Search word.
              paramType: query
              type: string
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
                    CardUserViewSet, self).list(
                        request,
                        queryset=self.get_queryset(user.id),
                        *args,
                        **kwards    )
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request, user_pk=None, *args, **kwargs):
        """
        Add card from user
        ---
        omit_parameters:
            - form
        parameters:
            - name: body
              pytype: CardSerializer
              paramType: body
              description:
                'name: <b>required</b> <br>
                email: <b>required</b> <br>
                mobilePhone: <b>required</b> <br>
                lastName:NOT required <br>
                mothersName: NOT required <br>
                age: NOT required <br>
                housePhone: NOT required'
            - name: Authorization
              description: Bearer {token}.
              required: true
              type: string
              paramType: header
        responseMessages:
            - code: 201
              message: CREATED
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
                serializer = CardSerializer(data=request.data)
                if serializer.is_valid():
                    card = conekta_sita.create_card(user=user, data=request.data)
                    if card is not None:
                        card_data = {
                            "last_four":card.last4,
                            "is_default":True,
                            "conekta_card":card.id,
                            "brand_card":card.brand,
                        }
                        fields = Card().get_fields()
                        Card.objects.register(
                            data=card_data, fields=fields, user=user)
                    return Response(status=status.HTTP_201_CREATED)
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @detail_route(["PUT"])
    def set_default(self, request, user_pk=None, pk=None, *args, **kwargs):
        """
        Add card from user
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
            if Card.objects.exists(pk=pk):
                card = Card.objects.get(id=pk)
                if card.user_id == user.id:
                    if has_permission(request.META, user):
                        card_default = conekta_sita.set_default_card(user=user, card=card)
                        card_default_old = Card.objects.get(is_default=True, user_id=user.id)
                        card_default_old.is_default = False
                        card_default_old.save()
                        card.is_default = True
                        card.save()
                        return Response(status=status.HTTP_200_OK)
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_404_NOT_FOUND)

class CardViewSet(
    base_mixins.ListModelMixin,
    base_mixins.RetrieveModelMixin,
    GenericViewSet):
    serializer_class =  CardSerializerModel
    retrieve_serializer_class = CardSerializerModel
    partial_update_serializer_class = CardSerializerModel
    update_serializer_class = CardSerializerModel
    permission_classes = (IsAuthenticated, )

    def get_queryset(self, *args, **kwargs):
        queryset = Card.objects.all()
        query_params = get_query_params(self.request)
        q = query_params.get('q')

        if q:
            queryset = queryset.filter(last_four__icontains=q)

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
            return super(
                CardViewSet, self).list(
                    request,
                    queryset=self.get_queryset(),
                    *args,
                    **kwards    )
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
        if Card.objects.exists(pk=pk):
            card = Card.objects.get(id=pk)
            if User.objects.exists_user(pk=card.user_id):
                user = User.objects.get(id=card.user_id)
                if has_permission(request.META, user):
                    return super(
                        CardViewSet, self).retrieve(
                            request,
                            pk=pk,
                            instance=card)
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
        if Card.objects.exists(pk=pk):
            card = Card.objects.get(id=pk)
            if User.objects.exists_user(pk=card.user_id):
                user = User.objects.get(id=card.user_id)
                if has_permission(request.META, user):
                    card_deleted = conekta_sita.delete_card(user=user, card=card)
                    card.delete()
                    card = Card.objects.filter(user_id=user.id)
                    if card:
                        card_default = conekta_sita.set_default_card(user=user, card=card[0])
                        card[0].is_default = True
                        card[0].save()
                    print card
                    return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_404_NOT_FOUND)

router.register_nested(
    r'users',
    r'cards',
    CardUserViewSet,
    parent_lookup_name='user',
    base_name='cards'
)
router.register(
    r'cards',
    CardViewSet,
    base_name='card'
)
