from django.db import models
from django.conf import settings

from sita.core.db.models import CatalogueMixin

# Create your models here.

class Patient(CatalogueMixin):
    """Create model Patient."""

    last_name = models.CharField(
        max_length=100
    )
    mothers_name = models.CharField(
        max_length=100)
    
    email = models.EmailField(
        max_length=254
    )
    age = models.IntegerField()
    mobile_phone = models.CharField(
        max_length=10
    )
    house_phone = models.CharField(
        max_length=10
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )
