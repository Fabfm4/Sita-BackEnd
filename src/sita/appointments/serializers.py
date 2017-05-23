from rest_framework import serializers
from django.core.serializers.python import Serializer
from .models import Appointment
from sita.users.models import User
from datetime import datetime
from calendar import weekday

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

class AppointmentListSerializerMonth(Serializer):
    def serialize(self, queryset, year, month, last_day_month=None,  **options):
        print queryset
        self.start_serialization()
        self.start_object(month,year)
        if queryset:
            last_day = None
            for query in queryset:
                day = query.date_appointment.day
                print day
                if last_day is None:
                    for x in range(1, day):
                        self.start_day(year, month, x)
                    last_day = day
                if last_day == day:
                    self.start_date(query)
                else:
                    self.start_day(year, month, last_day, has_dates=True)
                    for x in range(last_day + 1, day):
                        self.start_day(year, month, x)
                    self.start_date(query)
                    last_day = day
            self.start_day(year, month, last_day, has_dates=True)
            for x in range(last_day + 1, last_day_month+1):
                self.start_day(year, month, x)
        else:
            for x in range(1, last_day_month+1):
                self.start_day(year, month, x)
        self.end_object()
        self.end_serialization()
        return self.getvalue()

    def start_day(self, year, month, day, has_dates=False):
        week_day = weekday(year, month, day)
        self._days.append(
            {"day":day,
            "week_day":week_day,
            "has_dates":has_dates,
            "dates": self._dates})
        self._dates = []

    def start_date(self, appointment):
        self._dates.append(
            {"id":appointment.id,
            "patient_id":appointment.patient_id,
            "hour": appointment.date_appointment.hour})


    def start_serialization(self):
        self._month = None
        self._year = None
        self._current = None
        self._days = []
        self._dates = []
        self.objects=None


    def start_object(self, month, year):
        self._month = month
        self._year = year

    def end_object(self):
        self.objects = {
            "month":self._month,
            "year":self._year,
            "days": self._days}
