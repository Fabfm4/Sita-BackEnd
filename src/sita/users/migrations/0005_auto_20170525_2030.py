# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-05-25 20:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20170524_2009'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='next_mount_pay',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='subscription',
            name='next_pay_date',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='next_time_in_minutes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='expiration_date',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]