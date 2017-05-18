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
from rest_framework.decorators import detail_route

class CardViewSet(
    base_mixins.ListModelMixin,
    base_mixins.RetrieveModelMixin,
    base_mixins.CreateModelMixin,
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
                    CardViewSet, self).list(
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
                    fields = Card().get_fields()
                    Card.objects.register(
                        data=request.data, fields=fields, user=user)
                    return Response(status=status.HTTP_201_CREATED)
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, user_pk=None, pk=None,  *args, **kwards):
        """
        Show an specific card
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
                card = Card.objects.get(pk=pk)
                if card.user_id == user.id:
                    if has_permission(request.META, user):
                        return super(
                            CardViewSet, self).retrieve(
                                request,
                                pk=pk,
                                *args,
                                **kwards)
                    return Response(status=status.HTTP_401_UNAUTHORIZED)

        return Response(status=status.HTTP_404_NOT_FOUND)

    @detail_route(methods=['PUT'])
    def set_default_card(self, request, user_pk=None, pk=None, *args, **kwargs):
        """
        Assing some card like default.
        ---
        omit_serializer: true
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
                card = Card.objects.get(pk=pk)
                if card.user_id == user.id:
                    if has_permission(request.META, user):
                        oldCardDefault = Card.objects.get_card_default(user.id)
                        if oldCardDefault is not None:
                            oldCardDefault.is_default = False
                            oldCardDefault.save()
                        card.is_default = True
                        card.save()
                        return Response(status=status.HTTP_200_OK)
                    return Response(status=status.HTTP_401_UNAUTHORIZED)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, user_pk=None, pk=None):
        """
        Delete card
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
            - code: 422
              message: UNPROCESSABLE ENTITY
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
                card = Card.objects.get(pk=pk)
                if card.user_id == user.id:
                    if has_permission(request.META, user):
                        if card.is_default:
                            cards = Card.objects.filter(
                                user_id=user.id, is_default=False)
                            print(cards)
                            if cards:
                                newCardDefault = cards[0]
                                newCardDefault.is_default = True
                                newCardDefault.save()
                            else:
                                return Response(
                                    {"message":"Can't delete this card"},
                                    status=422)
                        card.delete()
                        return Response(status=status.HTTP_200_OK)
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_404_NOT_FOUND)

router.register_nested(
    r'users',
    r'cards',
    CardViewSet,
    parent_lookup_name='user',
    base_name='cards'
)
