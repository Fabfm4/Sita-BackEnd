# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.db import models

from sita.core.db.models import TimeStampedMixin

# Create your models here.
class SubscriptionManager(models.Manager):
    def register(self, data, fields, **extra_fields):
        print data
        for key in data:
            print key
            if any(key in s for s in fields):
                extra_fields.setdefault(key, data.get(key))

        subscription = self.model(
            **extra_fields
        )
        subscription.save()

        return subscription

    def exists(self, pk=None):
        try:
            subscription = Subscription.objects.get(id=pk)
            return True
        except Subscription.DoesNotExist:
            return False

class Subscription(TimeStampedMixin):
    """Create Subscription model."""

    title = models.CharField(
        max_length=254,
        null=False,
        blank=True
    )
    time_in_minutes = models.IntegerField()
    description = models.TextField(
        null=True,
        blank=True
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    objects = SubscriptionManager()

    def __unicode__(self):
        return self.get_full_name()

    def get_full_name(self):
        return "Subscription: {0}".format(self.title)

    def get_fields(self):
        list = []
        for field in Subscription._meta.fields:
            list.append(field.name)
        return list
