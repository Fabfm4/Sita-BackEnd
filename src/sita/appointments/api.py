from sita.core.api.viewsets import GenericViewSet
from rest_framework import status
from sita.api.v1.routers import router
from sita.core.api.viewsets.nested import NestedViewset
from rest_framework.permissions import IsAuthenticated
from .serializers import AppointmentSerializer, AppointmentSerializerModel, AppointmentListSerializerMonth
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
from datetime import datetime
from calendar import monthrange

class AppointmentViewSet(
    base_mixins.ListModelMixin,
    GenericViewSet):
    serializer_class =  AppointmentSerializerModel
    retrieve_serializer_class = AppointmentSerializerModel
    partial_update_serializer_class = AppointmentSerializerModel
    update_serializer_class = AppointmentSerializerModel
    create_serializer_class = AppointmentSerializerModel
    permission_classes = (IsAuthenticated, )

    def get_queryset(self, user_id=None, patient_id=None, *args, **kwargs):

        queryset = Appointment.objects.filter(user_id=user_id, patient_id=patient_id)
        print(datetime.now())
        queryset = queryset.extra(where=["date_appointment >= '{0}'".format(datetime.now())])

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
                if patient.is_active and patient.user_id==user.id:
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
            if Patient.objects.exists(pk=patient_pk):
                patient = Patient.objects.get(pk=patient_pk)
                if patient.is_active and patient.user_id==user.id:
                    if has_permission(request.META, user):
                        return super(
                            AppointmentViewSet, self).list(
                                request,
                                queryset=self.get_queryset(user.id, patient.id),
                                *args,
                                **kwards    )
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_404_NOT_FOUND)

class AppointmentMonthViewSet(
    base_mixins.ListModelMixin,
    GenericViewSet):
    serializer_class =  AppointmentSerializerModel
    retrieve_serializer_class = AppointmentSerializerModel
    partial_update_serializer_class = AppointmentSerializerModel
    update_serializer_class = AppointmentSerializerModel
    create_serializer_class = AppointmentSerializerModel
    permission_classes = (IsAuthenticated, )

    def list(self, request, user_pk=None, *args, **kwargs):
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
            - name: month
              description: Search word.
              paramType: query
              type: string
              required: true
            - name: year
              description: Search word.
              paramType: query
              type: string
              required: true
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
                query_params = get_query_params(request)
                try:
                    year = int(query_params.get('year'))
                except ValueError:
                    return Response({"year":"is not a number"},status=status.HTTP_400_BAD_REQUEST)
                try:
                    month = int(query_params.get('month'))
                except ValueError:
                    return Response({"month":"is not a number"},status=status.HTTP_400_BAD_REQUEST)

                if month > 12 or month < 1:
                    return Response({"month":"number month is not correct"}, status=status.HTTP_400_BAD_REQUEST)

                if year < 1:
                    return Response({"year":"number month is not correct"}, status=status.HTTP_400_BAD_REQUEST)

                query = construct_query_view_month(year=year, month=month)
                serializer = AppointmentListSerializerMonth()
                last_day_month = monthrange(year, month)
                data = serializer.serialize(queryset=query,year=year, month=month, last_day_month=last_day_month[1])
                print data
                return Response(data,status=status.HTTP_200_OK)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_404_NOT_FOUND)



class AppointmentDayViewSet(
    base_mixins.ListModelMixin,
    GenericViewSet):
    serializer_class =  AppointmentSerializerModel
    retrieve_serializer_class = AppointmentSerializerModel
    partial_update_serializer_class = AppointmentSerializerModel
    update_serializer_class = AppointmentSerializerModel
    create_serializer_class = AppointmentSerializerModel
    permission_classes = (IsAuthenticated, )

    def list(self, request, user_pk=None, patient_pk=None, *args, **kwargs):
        pass


class AppointmentWeekViewSet(
    base_mixins.ListModelMixin,
    GenericViewSet):
    serializer_class =  AppointmentSerializerModel
    retrieve_serializer_class = AppointmentSerializerModel
    partial_update_serializer_class = AppointmentSerializerModel
    update_serializer_class = AppointmentSerializerModel
    create_serializer_class = AppointmentSerializerModel
    permission_classes = (IsAuthenticated, )

    def list(self, request, user_pk=None, patient_pk=None, *args, **kwargs):
        pass
router.register_nested(
    r'patients',
    r'appointments',
    AppointmentViewSet,
    parent_lookup_name='patient',
    base_name='appointment',
    depth_level=2
)
router.register_nested(
    r'users',
    r'appointments_view_month',
    AppointmentMonthViewSet,
    parent_lookup_name='user',
    base_name='appointments_view_month'
)
router.register_nested(
    r'users',
    r'appointments_view_day',
    AppointmentDayViewSet,
    parent_lookup_name='user',
    base_name='appointments_view_day'
)
router.register_nested(
    r'users',
    r'appointments_view_week',
    AppointmentWeekViewSet,
    parent_lookup_name='user',
    base_name='appointments_view_week'
)
