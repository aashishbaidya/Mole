# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Ministry, Department, District, Office
office_models = [Ministry, Department, District, Office]

admin.site.register(office_models)

# Register your models here.
