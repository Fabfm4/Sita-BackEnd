# -*- coding: utf-8 -*-
import os
from hashlib import md5

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from multiprocessing.managers import BaseManager
from django.contrib.gis.db import models
# from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from sita.core.db.models import TimeStampedMixin

class UserManager(BaseUserManager):
    """Custom Manager for crete users"""

    def _create_user(self, email, password, **extra_fields):
        """ Create new Users. """

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            last_login = timezone.now(),
            **extra_fields
        )
        user.set_password(password)
        user.save()

        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create a user."""

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)



class DeviceManager(models.Manager):
    def register(self, device_token, device_os, user):
        device = Device()
        try:
            device = Device.objects.get(user_id=user.id, device_os=device_os)
        except Device.DoesNotExist:
            pass
        device.device_token = device_token
        device.device_os = device_os
        device.user_id=user.id
        device.save()

class User(AbstractBaseUser, PermissionsMixin):
    """Create custom model User."""

    name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    first_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    mothers_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    email = models.EmailField(
        max_length=254,
        unique=True
    )
    phone = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('is_active')
    )
    is_staff = models.BooleanField(
        default=True,
        verbose_name=_('is_staff')
    )
    activation_code = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    reset_pass_code = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    conekta_card = models.CharField(
        max_length=254,
        null=True,
        blank=True,
    )
    created_date = models.DateField(
        auto_now_add=True
    )
    updated_date = models.DateField(
        auto_now=True
    )
    has_subscription = models.BooleanField(
        default=False
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __unicode__(self):
        return self.get_full_name()

    def get_full_name(self):
        return "{0}".format(self.email)

    def get_short_name(self):
        return "{0}".format(self.name)

class Subscription(TimeStampedMixin):
    """ Create The subscriptions from User."""

    expiration_date = models.DateField(
        editable=False,
        blank=True,
        null=True
    )
    is_current = models.BooleanField(
        default=True
    )
    is_test = models.BooleanField(
        default=False
    )
    time_in_minutes = models.IntegerField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

class Device(TimeStampedMixin):
    """ Create The subscriptions from User."""

    TYPE_OS = (
        ('IOS', 'IOS'),
        ('ANDROID', 'ANDROID')
    )
    device_token = models.CharField(
        max_length=254,
        null=True,
        blank=True,
    )
    device_os = models.CharField(
        max_length=10,
        choices=TYPE_OS
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    objects = DeviceManager()

    def __unicode__(self):
        return self.get_full_name()

    def get_full_name(self):
        user = User.objects.get(id=self.user_id)
        return "{0} {1}".format(self.device_os, user.email)
