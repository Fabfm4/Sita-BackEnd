from sita.core.api.viewsets import GenericViewSet
from rest_framework import status
from sita.api.v1.routers import router
from sita.core.api.viewsets.nested import NestedViewset
from rest_framework.permissions import IsAuthenticated
from .serializers import NoteSerializer, NoteSerializerModel
from sita.patients.models import Patient
from sita.users.models import User
from .models import Note
from rest_framework.response import Response
from sita.utils.refresh_token import has_permission
from sita.core.api.mixins import base as base_mixins
from django.contrib.auth import get_user_model
from sita.utils.urlresolvers import get_query_params

class NotePatientViewSet(
    base_mixins.ListModelMixin,
    GenericViewSet):
    serializer_class =  NoteSerializerModel
    list_serializer_class =  NoteSerializerModel
    retrieve_serializer_class = NoteSerializerModel
    partial_update_serializer_class = NoteSerializerModel
    update_serializer_class = NoteSerializerModel
    permission_classes = (IsAuthenticated, )

    def get_queryset(self, patient_pk=None, *args, **kwargs):

        queryset = Note.objects.filter(patient_id=patient_pk)
        query_params = get_query_params(self.request)
        q = query_params.get('q')

        if q:
            queryset = queryset.filter(name__icontains=q)

        return queryset

    def list(self, request, patient_pk=None, *args, **kwards):
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
        if Patient.objects.exists(pk=patient_pk):
            patient = Patient.objects.get(id=patient_pk)
            if patient.is_active:
                if User.objects.exists_user(pk=patient.user_id):
                    user = User.objects.get(id=patient.user_id)
                    if has_permission(request.META, user):
                        return super(
                            NotePatientViewSet, self).list(
                                request,
                                queryset=self.get_queryset(patient.id),
                                *args,
                                **kwards    )
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request, patient_pk=None):
        """
        Create patient from user
        ---
        omit_parameters:
            - form
        parameters:
            - name: body
              pytype: NoteSerializer
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
            - code: 400
              message: BAD REQUEST
            - code: 500
              message: INTERNAL SERVER ERROR
        consumes:
            - application/json
        produces:
            - application/json
        """
        if Patient.objects.exists(pk=patient_pk):
            patient = Patient.objects.get(id=patient_pk)
            if patient.is_active:
                if User.objects.exists_user(pk=patient.user_id):
                    user = User.objects.get(id=patient.user_id)
                    if has_permission(request.META, user):
                        serializer = NoteSerializer(data=request.data)
                        if serializer.is_valid():
                            fields = Note().get_fields()
                            Note.objects.register(
                                data=request.data, fields=fields, patient=patient)
                            return Response(status=status.HTTP_201_CREATED)
                        return Response(
                            serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_404_NOT_FOUND)

class NoteViewSet(
    base_mixins.ListModelMixin,
    base_mixins.RetrieveModelMixin,
    base_mixins.PartialUpdateModelMixin,
    GenericViewSet):
    serializer_class =  NoteSerializerModel
    retrieve_serializer_class = NoteSerializerModel
    partial_update_serializer_class = NoteSerializerModel
    update_serializer_class = NoteSerializerModel
    permission_classes = (IsAuthenticated, )


    def get_queryset(self, *args, **kwargs):
        queryset = Note.objects.all()
        query_params = get_query_params(self.request)
        q = query_params.get('q')

        if q:
            queryset = queryset.filter(title__icontains=q)

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
                NoteViewSet, self).list(
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
        if Note.objects.exists(pk=pk):
            note = Note.objects.get(id=pk)
            if Patient.objects.exists(pk=note.patient_id):
                patient = Patient.objects.get(id=pk)
                if User.objects.exists_user(pk=patient.user_id):
                    user = User.objects.get(id=patient.user_id)
                    if has_permission(request.META, user):
                        return super(
                            NoteViewSet, self).retrieve(
                                request,
                                pk=pk,
                                instance=note)
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        """
        Update information from an specific patient
        ---
        omit_parameters:
            - form
        parameters:
            - name: body
              pytype: NoteSerializer
              paramType: body
              description:
                'name: NOT required <br>
                lastName: NOT required <br>
                mothersName: NOT required <br>
                email: NOT required <br>
                age: NOT required <br>
                mobilePhone: NOT required <br>
                housePhone: NOT required'
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

        if Note.objects.exists(pk=pk):
            note = Note.objects.get(id=pk)
            if Patient.objects.exists(pk=note.patient_id):
                patient = Patient.objects.get(id=pk)
                if User.objects.exists_user(pk=patient.user_id):
                    user = User.objects.get(id=patient.user_id)
                    if has_permission(request.META, user):
                        return super(NoteViewSet, self).partial_update(request, pk, note)
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
        if Note.objects.exists(pk=pk):
            note = Note.objects.get(id=pk)
            if Patient.objects.exists(pk=note.patient_id):
                patient = Patient.objects.get(id=pk)
                if User.objects.exists_user(pk=patient.user_id):
                    user = User.objects.get(id=patient.user_id)
                    if has_permission(request.META, user):
                        note.delete()
                        return Response(status=status.HTTP_200_OK)
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_404_NOT_FOUND)

router.register_nested(
    r'patients',
    r'notes',
    NotePatientViewSet,
    parent_lookup_name='patient',
    base_name='notes'
)
router.register(
    r'notes',
    NoteViewSet,
    base_name='note'
)
