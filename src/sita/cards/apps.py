from django.apps import AppConfig
from django.db.models.signals import post_save


class CardsAppConfig(AppConfig):
    """
    AppConfig for the ```sita.cards``` module.
    """
    name = 'sita.cards'
    def ready(self):
        super(CardsAppConfig, self).ready()

        model = self.get_model('Card')
