# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.db.models.signals import post_save

class UsersAppConfig(AppConfig):
    """
    AppConfig for the ```sita.users``` module.
    """
    name = 'sita.users'
    def ready(self):
        super(UsersAppConfig, self).ready()

        model = self.get_model('User')
