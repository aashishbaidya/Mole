from django.core.management.base import BaseCommand
from django.contrib.auth.models import User,Group
from userrole.models import UserRole


class Command(BaseCommand):
    help = 'Provide a username , creates a Super Admin role'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)

    def handle(self, *args, **options):
        username = options['username']
        self.stdout.write(username)
        super_admin = Group.objects.get(name="Super Admin")

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            self.stdout.write('user found')
            role, created = UserRole.objects.get_or_create(user=user, group=super_admin)

            if created:
                self.stdout.write('new super admin role created for user')
            else:
                self.stdout.write('super admin role already exists for user')

        else:
            self.stdout.write('user not found.. "%s"', username),



 




