# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-20 17:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_office'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='office',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_office', to='office.Office'),
        ),
    ]