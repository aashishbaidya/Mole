from __future__ import unicode_literals

from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models

from office.models import Office



class UserRole(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_roles')
    group = models.ForeignKey(Group)
    office = models.ForeignKey(Office, related_name='office_roles', blank=True, null=True)
    started_at = models.DateTimeField(default=datetime.now)
    ended_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return 'user: {}\'s role : {}'.format(self.user.__unicode__(), self.group.__unicode__())

    class Meta:
        unique_together = ('user', 'group', 'office')

    def clean(self):
        if self.group.name in ['Office Head', 'Information Officer'] and not self.office_id:
            raise ValidationError({
                'company': ValidationError(_('Missing Office.'), code='required'),
            })


        if self.user and UserRole.objects.filter(user=self.user, group=self.group, office=self.office).exists():
            raise ValidationError({
                'user': ValidationError(_('User Role Already Exists.')),
            })

    def save(self, *args, **kwargs):
        if self.group.name in ['Super Admin', 'Admin Assistant']:
            self.office = None
        super(UserRole, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        if self.group.name in ['Super Admin', 'Admin Assistant']:
            self.office = None
        super(UserRole, self).update(*args, **kwargs)

    @staticmethod
    def is_active(user, group):
        return UserRole.objects.filter(user=user, group__name=group, ended_at=None).exists()

    @staticmethod
    def get_active_roles(user):
        return UserRole.objects.filter(user=user, ended_at=None).select_related('group', 'office')

    @staticmethod
    def get_active_office_roles(user, office):
        return UserRole.objects.filter(user=user, office=office, ended_at=None, group__name__in= []).\
            select_related('group', 'office')

