# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.db.models.signals import post_save

class NotesAppConfig(AppConfig):
    """
    AppConfig for the ```sita.notes``` module.
    """
    name = 'sita.notes'
    def ready(self):
        super(NotesAppConfig, self).ready()

        model = self.get_model('Note')
