# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.db import models

from sita.core.db.models import TimeStampedMixin

# Create your models here.
class Payment(TimeStampedMixin):
    """Create Payment model."""

    amount = models.DecimalField(
        max_digits=7,
        decimal_places=2
    )
    conekta_pay_code = models.CharField(
        max_length=254
    )
    description = models.TextField()
    last_four = models.CharField(
        max_length=4
    )
    title_subscription = models.CharField(
        max_length=50
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )
    is_default = models.BooleanField(
        default=False
    )
