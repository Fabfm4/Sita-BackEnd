from django.db import models
from django.conf import settings

from sita.core.db.models import CatalogueMixin

# Create your models here.
class PatientManager(models.Manager):
    def register(self, data, fields, user, **extra_fields):
        print data
        for key in data:
            print key
            if any(key in s for s in fields):
                extra_fields.setdefault(key, data.get(key))

        patient = self.model(
            user_id=user.id,
            **extra_fields
        )
        patient.save()

        return patient

    def exists(self, pk=None):
        try:
            user = Patient.objects.get(id=pk)
            return True
        except User.DoesNotExist:
            return False


class Patient(CatalogueMixin):
    """Create model Patient."""

    last_name = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    mothers_name = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    email = models.EmailField(
        max_length=254,
    )
    age = models.IntegerField(
        null=True,
        blank=True
    )
    mobile_phone = models.CharField(
        max_length=10,
    )
    house_phone = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    objects = PatientManager()

    def get_fields(self):
        list = []
        for field in Patient._meta.fields:
            list.append(field.name)
        return list
