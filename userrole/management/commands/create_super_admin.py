from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User
from django.db import transaction

from userrole.models import UserRole

class Command(BaseCommand):
    help = 'Create default super Admin'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="Super Admin")
        with transaction.atomic():
            user = User.objects.create_user('admin', 'admin@mole.com', 'admin@admin123')
            user.is_staff=True
            user.save()
            role = UserRole(user=user, group=group)
            role.save()
        self.stdout.write('Successfully created Super Admin .')