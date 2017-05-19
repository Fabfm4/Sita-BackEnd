# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.db import models

from sita.core.db.models import TimeStampedMixin

# Create your models here.ç
class NoteManager(models.Manager):
    def register(self, data, fields, patient, **extra_fields):
        print data
        for key in data:
            print key
            if any(key in s for s in fields):
                extra_fields.setdefault(key, data.get(key))

        note = self.model(
            patient_id=patient.id,
            **extra_fields
        )
        note.save()

        return note

    def exists(self, pk=None):
        try:
            note = Note.objects.get(id=pk)
            return True
        except Note.DoesNotExist:
            return False

class Note(TimeStampedMixin):
    """Create Notes model"""

    title = models.CharField(
        max_length=150
    )
    content = models.TextField(
        null=True,
        blank=True
    )
    patient = models.ForeignKey(
        'patients.patient',
        on_delete=models.PROTECT
    )

    objects = NoteManager()

    def get_fields(self):
        list = []
        for field in Note._meta.fields:
            list.append(field.name)
        return list
