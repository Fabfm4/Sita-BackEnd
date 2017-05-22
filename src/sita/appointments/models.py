# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.db import models

from sita.core.db.models import TimeStampedMixin

# Create your models here.
class AppointmentManager(models.Manager):
    def register(self, data, fields, user, **extra_fields):
        for key in data:
            if any(key in s for s in fields):
                extra_fields.setdefault(key, data.get(key))

        appointment = self.model(
            user_id=user.id,
            **extra_fields
        )

        appointment.save()

        return card

    def exists(self, pk=None):
        try:
            appointment = Appointment.objects.get(id=pk)
            return True
        except Appointment.DoesNotExist:
            return False

class Appointment(TimeStampedMixin):
    subject = models.CharField(
        max_length=254
    )
    date_appointment = models.DateField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )
    patient = models.ForeignKey(
        'patients.patient',
        on_delete=models.PROTECT
    )
    duration_hours = models.IntegerField()


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
