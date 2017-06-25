# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from office.models import Office

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	email_confirmed = models.BooleanField(default=False)
	name = models.CharField(max_length=30, blank=True)
	phoneno = models.CharField(max_length=30, blank=True)
	assign_date = models.DateField(null=True, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	photo = models.ImageField(null=True, blank=True)
	office = models.ForeignKey(Office, related_name='user_office', null=True, blank=True)
	def __str__(self):
		return str(self.user)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
