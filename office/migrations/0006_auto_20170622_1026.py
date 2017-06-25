# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-22 10:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0005_auto_20170622_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='municipalitydetail',
            name='sub_mayor_address',
            field=models.CharField(blank=True, max_length=30, verbose_name='\u0909\u092a-\u092e\u092f\u0947\u0930/\u0905\u0927\u094d\u092f\u0915\u094d\u0937\u0915\u094b \u0920\u0947\u0917\u093e\u0928\u093e '),
        ),
        migrations.AlterField(
            model_name='municipalitydetail',
            name='sub_mayor_name',
            field=models.CharField(max_length=30, verbose_name='\u0909\u092a-\u092e\u092f\u0947\u0930/\u0905\u0927\u094d\u092f\u0915\u094d\u0937\u0915\u094b \u0928\u093e\u092e'),
        ),
        migrations.AlterField(
            model_name='municipalitydetail',
            name='sub_mayor_phone_no',
            field=models.CharField(max_length=30, verbose_name='\u0909\u092a-\u092e\u092f\u0947\u0930/\u0905\u0927\u094d\u092f\u0915\u094d\u0937\u0915\u094b \u092b\u094b\u0928'),
        ),
        migrations.AlterField(
            model_name='municipalitydetail',
            name='ward_chief_details',
            field=models.TextField(blank=True, verbose_name='\u0935\u0921\u093e \u092a\u094d\u0930\u092e\u0941\u0916\u0915\u094b \u0935\u093f\u0935\u0930\u0923 '),
        ),
    ]