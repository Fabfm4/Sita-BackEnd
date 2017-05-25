from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from celery.decorators import task

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sita.settings')
app = Celery('sita')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
