from rest_framework import serializers
from .models import Appointment
from sita.users.models import User

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
                'user' )
