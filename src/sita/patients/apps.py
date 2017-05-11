# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.db.models.signals import post_save

class PatientsAppConfig(AppConfig):
    """
    AppConfig for the ```sita.patients``` module.
    """
    name = 'sita.patients'
    def ready(self):
        super(PatientsAppConfig, self).ready()

        model = self.get_model('Patient')
