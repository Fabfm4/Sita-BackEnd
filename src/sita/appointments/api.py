from sita.core.api.viewsets import GenericViewSet
from rest_framework import status
from sita.api.v1.routers import router
from sita.core.api.viewsets.nested import NestedViewset
from rest_framework.permissions import IsAuthenticated
from .serializers import AppointmentSerializer, AppointmentSerializerModel
from sita.users.api import UserViewSet
from sita.appointments.models import Appointment
from sita.patients.models import Patient
from sita.users.models import User
from rest_framework.response import Response
from sita.utils.refresh_token import has_permission
from sita.core.api.mixins import base as base_mixins
from django.contrib.auth import get_user_model
from sita.utils.urlresolvers import get_query_params
from rest_framework.decorators import detail_route
from sita.utils.appointmentQuery import construct_query_view_month

class AppointmentViewSet(
    base_mixins.ListModelMixin,
    GenericViewSet):
    serializer_class =  AppointmentSerializerModel
    retrieve_serializer_class = AppointmentSerializerModel
    partial_update_serializer_class = AppointmentSerializerModel
    update_serializer_class = AppointmentSerializerModel
    create_serializer_class = AppointmentSerializerModel
    permission_classes = (IsAuthenticated, )

    def get_queryset(self, user_id=None, *args, **kwargs):
        queryset = Appointment.objects.filter(user_id=user_id)
        query_params = get_query_params(self.request)
        view = query_params.get('view')
        year = query_params.get('year')
        month = query_params.get('month')
        date = query_params.get('date')
        week = query_params.get('week')
        if view == "month":
            if not year:
                return Response("if you select view like month you should send the year", status=status.HTTP_400_BAD_REQUEST)
            if not month:
                return Response("if you select view like month you should send the month", status=status.HTTP_400_BAD_REQUEST)
            construct_query_view_month(query, year, month)
        if view == "week":
            if not year:
                return Response({"year":"if you select view like month you should send the year"}, status=status.HTTP_400_BAD_REQUEST)
            if not week:
                return Response({"month":"if you select view like month you should send the week"}, status=status.HTTP_400_BAD_REQUEST)
        if view == "day":
            if not date:
                return Response({"month":"if you select view like month you should send the week"}, status=status.HTTP_400_BAD_REQUEST)

        return queryset

    def create(self, request, user_pk=None, patient_pk=None, *args, **kwargs):
        """
        Add card from user
        ---
        omit_parameters:
            - form
        parameters:
            - name: body
              pytype: AppointmentSerializer
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
            if Patient.objects.exists(pk=patient_pk):
                patient = Patient.objects.get(pk=patient_pk)
                if patient.is_active:
                    if has_permission(request.META, user):
                        serializer = AppointmentSerializer(data=request.data)
                        if serializer.is_valid():
                            fields = Appointment().get_fields()
                            appointment = Appointment.objects.register(
                                data=request.data, fields=fields, user=user, patient=patient)
                            if appointment:
                                return Response(status=status.HTTP_201_CREATED)
                            else:
                                return Response({"message": "Exist a date in the same time"},status=422)
                        return Response(
                            serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_404_NOT_FOUND)


    def list(self, request, user_pk=None, patient_pk=None, *args, **kwards):
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
            - name: view
              description: Search word.
              paramType: query
              type: string
              enum: [month, week, day]
            - name: year
              description: Search word.
              paramType: query
              type: integer
            - name: month
              description: Search word.
              paramType: query
              type: integer
            - name: week
              description: Search word.
              paramType: query
              type: integer
            - name: day
              description: Search word.
              paramType: query
              type: date
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
            if Patient.objects.exists(pk=patient_pk):
                patient = Patient.objects.get(pk=patient_pk)
                if patient.is_active:
                    if has_permission(request.META, user):
                        return super(
                            AppointmentViewSet, self).list(
                                request,
                                queryset=self.get_queryset(user.id),
                                *args,
                                **kwards    )
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_404_NOT_FOUND)


router.register_nested(
    r'patients',
    r'appointments',
    AppointmentViewSet,
    parent_lookup_name='patient',
    base_name='appointment',
    depth_level=2
)
