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
        max_length=254
    )
    time_in_minutes = models.IntegerField()
    description = models.TextField(
        null=True,
        blank=True
    )

    objects = SubscriptionManager()

    def get_fields(self):
        list = []
        for field in Subscription._meta.fields:
            list.append(field.name)
        return list
