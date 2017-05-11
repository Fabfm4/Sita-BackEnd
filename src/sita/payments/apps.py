# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.db.models.signals import post_save

class PaymentsAppConfig(AppConfig):
    """
    AppConfig for the ```sita.payments``` module.
    """
    name = 'sita.payments'
    def ready(self):
        super(PaymentsAppConfig, self).ready()

        model = self.get_model('Payment')
