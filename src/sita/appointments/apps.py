# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.db.models.signals import post_save

class AppointmentsAppConfig(AppConfig):
    """
    AppConfig for the ```sita.appointments``` module.
    """
    name = 'sita.appointments'
    def ready(self):
        super(AppointmentsAppConfig, self).ready()

        model = self.get_model('Appointment')
