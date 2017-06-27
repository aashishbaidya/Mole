# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from office.models import Office,Department

class Command(BaseCommand):
    help = 'Create default Offices'

    def handle(self, *args, **options):
        dep1, created = Department.objects.get_or_create(pk="1")

        office_list = ['वैदेशिक रोजगार विभाग ', 'श्रम विभाग', 'वैदेशिक रोजगार प्रवर्द्धन वोर्ड', 'व्यवसायिक तथा सीप विकास तालिम केन्द्र','व्यवसायजन्य सुरक्षा तथा स्वास्थ्य सम्बन्धी आयोजना','ई. पि. एस. कोरिया शाखा','सामाजिक सुरक्षा कोष ','वैदेशिक रोजगार न्यायधिकरण']
        for office in office_list:
            new_office, created = Office.objects.get_or_create(name=office, department=dep1)
            if created:
                self.stdout.write('Successfully created office .. "%s"' % office)