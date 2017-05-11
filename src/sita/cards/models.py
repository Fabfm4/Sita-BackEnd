# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.db import models
from sita.core.db.models import TimeStampedMixin
# Create your models here.

class Card(TimeStampedMixin):
    """Create model Card"""

    last_four = models.CharField(
        max_length=4
    )
    TYPE_CARDS = (
        ('1', 'VISA'),
        ('2', 'MASTERCARD'),
        ('3', 'AMEX'),
    )
    type_card = models.CharField(
        max_length=1,
        choices=TYPE_CARDS)
    conekta_card = models.CharField(
        max_length=254
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )
