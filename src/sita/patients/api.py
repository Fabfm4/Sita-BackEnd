from sita.core.api.viewsets import GenericViewSet
from rest_framework import status
from sita.api.v1.routers import router
from sita.core.api.viewsets.nested import NestedViewset
from rest_framework.permissions import IsAuthenticated
from .serializers import PatientSerializer, PatientSerializerModel
from sita.users.api import UserViewSet
from sita.patients.models import Patient
from sita.users.models import User
from rest_framework.response import Response
from sita.utils.refresh_token import has_permission
from sita.core.api.mixins import base as base_mixins
from django.contrib.auth import get_user_model
from sita.utils.urlresolvers import get_query_params

class PatientViewSet(
    base_mixins.ListModelMixin,
    base_mixins.RetrieveModelMixin,
    GenericViewSet):
    serializer_class =  PatientSerializerModel
    retrieve_serializer_class = PatientSerializerModel
    update_serializer_class = PatientSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self, user_id=None, *args, **kwargs):

        queryset = Patient.objects.all()
        if user_id is not None:
            queryset = Patient.objects.filter(user_id=user_id)
        query_params = get_query_params(self.request)
        q = query_params.get('q')

        if q:
            queryset = queryset.filter(email__contains=q)

        return queryset

    def list(self, request, user_pk=None, *args, **kwards):
        """
        Create user by Admin.
        ---
        omit_parameters:
            - form
        parameters:
            - name: body
              pytype: PatientSerializer
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
        if User.objects.exists_user(pk=user_pk):
            user = User.objects.get(id=user_pk)
            if has_permission(request.META, user):
                return super(
                    PatientViewSet, self).list(
                        request,
                        queryset=self.get_queryset(user.id),
                        *args,
                        **kwards    )
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request, user_pk=None):
        """
        Create user by Admin.
        ---
        omit_parameters:
            - form
        parameters:
            - name: body
              type: PatientSerializer
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
        if User.objects.exists_user(pk=user_pk):
            user = User.objects.get(id=user_pk)
            if has_permission(request.META, user):
                serializer = PatientSerializer(data=request.data)
                if serializer.is_valid():
                    fields = Patient().get_fields()
                    Patient.objects.register(
                        data=request.data, fields=fields, user=user)
                    return Response(status=status.HTTP_201_CREATED)
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, user_pk=None, pk=None,  *args, **kwards):
        """
        Create user by Admin.
        ---
        omit_parameters:
            - form
        parameters:
            - name: body
              type: PatientSerializer
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
        if User.objects.exists_user(pk=user_pk):
            user = User.objects.get(id=user_pk)
            if Patient.objects.exists(pk=pk):
                patient = Patient.objects.get(pk=pk)
                if patient.user_id == user.id:
                    if has_permission(request.META, user):
                        return super(
                            PatientViewSet, self).retrieve(
                                request,
                                pk=pk,
                                *args,
                                **kwards)
                    return Response(status=status.HTTP_401_UNAUTHORIZED)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, user_pk=None, pk=None):
        """
        Create user by Admin.
        ---
        omit_parameters:
            - form
        parameters:
            - name: body
              type: PatientSerializer
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
        if User.objects.exists_user(pk=user_pk):
            user = User.objects.get(id=user_pk)
            if Patient.objects.exists(pk=pk):
                patient = Patient.objects.get(pk=pk)
                if patient.user_id == user.id:
                    if has_permission(request.META, user):
                        return Response()
                    return Response(status=status.HTTP_401_UNAUTHORIZED)

        return Response(status=status.HTTP_404_NOT_FOUND)


router.register_nested(
    r'users',
    r'patient',
    PatientViewSet,
    parent_lookup_name='user',
    base_name='patient'
)
