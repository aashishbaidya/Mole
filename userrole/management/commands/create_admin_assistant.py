from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User
from django.db import transaction

from userrole.models import UserRole


class Command(BaseCommand):
    help = 'Create default Admin Assistant'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="'Admin Assistant")
        with transaction.atomic():
            user = User.objects.create_user('adminassistant', 'adminassistant@mole.com', 'adminassistant@123')
            user.save()
            role = UserRole(user=user, group=group)
            role.save()
        self.stdout.write('Successfully created Admin Assistant .')