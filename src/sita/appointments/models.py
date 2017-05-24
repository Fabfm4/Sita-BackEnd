# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.db import models
from sita.users.models import User
from datetime import datetime, timedelta

from sita.core.db.models import TimeStampedMixin

# Create your models here.
class AppointmentManager(models.Manager):
    def register(self, data, fields, user, patient, **extra_fields):
        for key in data:
            if any(key in s for s in fields):
                extra_fields.setdefault(key, data.get(key))
        hours = data.get("duration_hours")
        date_init = datetime.strptime(data.get("date_appointment"), "%Y-%m-%dT%H:%M:%S")
        date_end = date_init + timedelta(hours=hours,minutes=00)
        if self.exists_middel_date_init(date=date_init, user_id=user.id) or self.exists_middel_date_end(date=date_end, user_id=user.id) or self.exists_middel_dates(date_init=date_init, date_end=date_end, user_id=user.id):
            return None
        else:
            appointment = self.model(
                user_id=user.id,
                patient_id=patient.id,
                **extra_fields
            )
            appointment.save()

            return appointment

    def exists(self, pk=None):
        try:
            appointment = Appointment.objects.get(id=pk)
            return True
        except Appointment.DoesNotExist:
            return False

    def exists_middel_date_init(self, date, user_id):
        appointments = Appointment.objects.extra(
        where=["date_appointment <= '{0}' and date_appointment + (duration_hours  || ' hours')::interval > '{0}'".format(date), "user_id = {0}".format(user_id)])
        print(appointments)
        print(date)
        print("init")
        return appointments

    def exists_middel_date_end(self, date, user_id):
        appointments = Appointment.objects.extra(
        where=["date_appointment < '{0}' and date_appointment + (duration_hours  || ' hours')::interval >= '{0}'".format(date), "user_id = {0}".format(user_id)])
        print(appointments)
        print(date)
        print("end")
        return appointments

    def exists_middel_dates(self, date_init, date_end, user_id):
        appointments = Appointment.objects.extra(
        where=["date_appointment >= '{0}' and date_appointment + (duration_hours  || ' hours')::interval <= '{1}'".format(date_init, date_end), "user_id = {0}".format(user_id)])
        print(appointments)
        print("dates")
        return appointments

class Appointment(TimeStampedMixin):
    subject = models.CharField(
        max_length=254
    )
    date_appointment = models.DateTimeField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )
    patient = models.ForeignKey(
        'patients.patient',
        on_delete=models.PROTECT
    )
    duration_hours = models.IntegerField()

    time_zone = models.CharField(
        max_length=254,
        default='')


    objects = AppointmentManager()

    def get_fields(self):
        list = []
        for field in Appointment._meta.fields:
            list.append(field.name)
        return list

    def __unicode__(self):
        return self.get_full_name()

    def get_full_name(self):
        user = User.objects.get(id=self.user_id)
        return "Card: {0} from {1}".format(self.subject, user.email)
