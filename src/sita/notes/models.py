# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.db import models

from sita.core.db.models import TimeStampedMixin

# Create your models here.

class Note(TimeStampedMixin):
    """Create Notes model"""

    title = models.CharField(
        max_length=150
    )
    content = models.TextField(
        null=True,
        blank=True
    )
    patient = models.ForeignKey(
        'patients.patient',
        on_delete=models.PROTECT
    )
    appointment = models.ForeignKey(
        'appointments.appointment',
        on_delete=models.PROTECT
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )
