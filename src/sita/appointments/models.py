# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.db import models

from sita.core.db.models import TimeStampedMixin

# Create your models here.

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
