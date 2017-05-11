# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.db import models

from sita.core.db.models import TimeStampedMixin

# Create your models here.

class Subscription(TimeStampedMixin):
    """Create Subscription model."""

    title = models.CharField(
        max_length=254
    )
    time_in_minutes = models.IntegerField()
    description = models.TextField(
        null=True,
        blank=True
    )
