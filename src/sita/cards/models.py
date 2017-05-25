# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.db import models
from sita.core.db.models import TimeStampedMixin
from sita.users.models import User

# Create your models here.
class CardManager(models.Manager):
    def register(self, data, fields, user, **extra_fields):
        for key in data:
            if any(key in s for s in fields):
                extra_fields.setdefault(key, data.get(key))

        card = self.model(
            user_id=user.id,
            **extra_fields
        )
        if self.get_card_default(user_pk=user.id) is not None:
            card.is_default = False
        card.save()

        return card

    def exists(self, pk=None):
        try:
            card = Card.objects.get(id=pk)
            return True
        except Card.DoesNotExist:
            return False

    def get_card_default(self, user_pk=None):
        try:
            card = Card.objects.get(user_id = user_pk, is_default=True)
            return card
        except Card.DoesNotExist:
            return None


class Card(TimeStampedMixin):
    """Create model Card"""

    last_four = models.CharField(
        max_length=4
    )
    BRAND_CARDS = (
        ('VISA', 'VISA'),
        ('MC', 'MASTERCARD'),
        ('AMERICAN_EXPRESS', 'AMERICAN EXPRESS'),
    )
    brand_card = models.CharField(
        max_length=100,
        choices=BRAND_CARDS)
    conekta_card = models.CharField(
        max_length=254
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )
    is_default = models.BooleanField(
        default=True
    )

    objects = CardManager()

    def get_fields(self):
        list = []
        for field in Card._meta.fields:
            list.append(field.name)
        return list

    def __unicode__(self):
        return self.get_full_name()

    def get_full_name(self):
        user = User.objects.get(id=self.user_id)
        return "Card: {0} from {1}".format(self.last_four, user.email)
