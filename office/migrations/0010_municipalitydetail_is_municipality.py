# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-25 06:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0009_auto_20170624_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='municipalitydetail',
            name='is_municipality',
            field=models.BooleanField(default=True),
        ),
    ]
