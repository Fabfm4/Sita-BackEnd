from django.contrib import admin

from . import models

# Register your models here.

admin.site.register(models.User)
admin.site.register(models.Subscription)
admin.site.register(models.Device)

# Register your models here.
