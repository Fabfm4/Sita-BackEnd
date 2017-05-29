# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.db import models
from sita.core.db.models import TimeStampedMixin
from sita.users.models import User, Subscription

# Create your models here.
class PaymentManager(models.Manager):
    def register(self, data, fields, user, **extra_fields):
        for key in data:
            if any(key in s for s in fields):
                extra_fields.setdefault(key, data.get(key))

        payment = self.model(
            user_id=user.id,
            **extra_fields
        )
        payment.save()

        return payment

    def exists(self, pk=None):
        try:
            payment = Payment.objects.get(id=pk)
            return True
        except Payment.DoesNotExist:
            return False

class Payment(TimeStampedMixin):
    """Create Payment model."""

    BRAND_CARDS = (
        ('VISA', 'VISA'),
        ('MC', 'MASTERCARD'),
        ('AMERICAN_EXPRESS', 'AMERICAN EXPRESS'),
    )
    conekta_id = models.CharField(
        max_length=255,
        null=True
    )
    card_last_four = models.CharField(
        max_length=4,
        null=True
    )
    card_brand = models.CharField(
        max_length=10,
        choices=BRAND_CARDS,
        null=True
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    description = models.TextField()
    reference_id_conekta = models.CharField(
        max_length=255,
        null=True)
    currency = models.CharField(
        max_length=10
    )
    title_subscription = models.CharField(
        max_length=254
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )
    subscription = models.ForeignKey(
        'users.subscription',
        on_delete=models.PROTECT,
        null=True
    )
    fail = models.BooleanField(
        default=False
    )

    objects = PaymentManager()

    def get_fields(self):
        list = []
        for field in Payment._meta.fields:
            list.append(field.name)
        return list

    def __unicode__(self):
        return self.get_full_name()

    def get_full_name(self):
        user = User.objects.get(id=self.user_id)
        return "Payment: {0} from {1}".format(self.title_subscription, user.email)
