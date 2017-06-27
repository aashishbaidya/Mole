# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from office.models import Ministry

class Command(BaseCommand):
    help = 'Create default Ministry'

    def handle(self, *args, **options):
        Ministry_list = ['ministry1 ', 'ministry2', ]
        for ministry in Ministry_list:
            new_ministry, created = Ministry.objects.get_or_create(name=ministry)
            if created:
                self.stdout.write('Successfully created ministry .. "%s"' % ministry)