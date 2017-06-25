# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserDetailsForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('password1', 'password2',)