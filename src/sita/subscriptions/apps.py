# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.db.models.signals import post_save

class SubscriptionsAppConfig(AppConfig):
    """
    AppConfig for the ```sita.subscription``` module.
    """
    name = 'sita.subscriptions'
    def ready(self):
        super(SubscriptionsAppConfig, self).ready()

        model = self.get_model('Subscription')
