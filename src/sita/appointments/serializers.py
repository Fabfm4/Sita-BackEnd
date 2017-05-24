from rest_framework import serializers
from django.core.serializers.python import Serializer
from .models import Appointment
from sita.users.models import User
from datetime import datetime
from calendar import weekday
from datetime import datetime, timedelta
import pytz

class AppointmentSerializer(serializers.Serializer):
    """"""
    subject = serializers.CharField(
        required = True,
        max_length=254
    )
    date_appointment = serializers.DateTimeField(
        required = True
    )
    duration_hours = serializers.IntegerField(
        required = True
    )
    time_zone = serializers.CharField(
        required = False
    )

    def validate(self, data):
        if data.get("time_zone") is not None:
            try:
                datetime.now(pytz.timezone(data.get("time_zone")))
            except pytz.UnknownTimeZoneError:
                raise serializers.ValidationError(
                    {"time_zone":"The time zone is not correct"})

        return data

class AppointmentSerializerModel(serializers.ModelSerializer):
    """
    Serializer used to return the proper token, when the user was succesfully
    logged in.
    """

    class Meta:
        model = Appointment
        fields = ('id',
                'subject',
                'date_appointment',
                'duration_hours',
                'patient',
                'user' ,
                'time_zone' )

class AppointmentListSerializer(Serializer):
    def end_object( self, obj ):
        self._current['id'] = obj._get_pk_val()
        self.objects.append( self._current )
