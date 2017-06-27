# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
from .imagecropper import PhotoForm
from django.shortcuts import render
from django.contrib.auth.models import User

from django.contrib.auth import login, authenticate
from django.views.generic import View
# from .tokens import account_activation_token
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from .models import Profile
from .forms import UserDetailsForm
from userrole.forms import UserRoleForm
from userrole.mixins import LoginRequiredMixin, SuperAdminMixin, CreateView, UpdateView, DeleteView
from userrole.models import UserRole as Role, UserRole

from django.shortcuts import redirect
from django.urls import reverse_lazy

class UserRoleView(object):
    model = UserRole
    success_url = reverse_lazy('role:user-role-list')
    form_class = UserRoleForm         



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None


    if user is not None and account_activation_token.check_token(user, token):

        profile = get_object_or_404(Profile, user=uid)
        photoform = PhotoForm(request.POST or None, instance=profile)
        userform = UserDetailsForm()


        return render(request, 'profiledetails.html', {'uid': uidb64, 'photoform':photoform, 'userform':userform})
    else:
    	return redirect('users:login')

    		#return redirect('question_detail', pk=question.pk)
    	#return redirect('supa:listoffice')





def firstlogin(request, *args, **kwargs):

    if request.method=='POST':

    	password1 = request.POST.get('password1')
    	password2 = request.POST.get('password2')

    	if password2 == password1:
        	usrid = request.POST.get('uidb64')
        	uid = force_text(urlsafe_base64_decode(usrid))
        	user = User.objects.get(pk=uid)
        	user.profile.email_confirmed = True
        	user.set_password(password2)
        	user.is_active = True
        	user.save()

                office = user.profile.office.id

                profile = get_object_or_404(Profile, user=uid)
            	user1 = authenticate(username=user.username, password=password2)
            	form = PhotoForm(request.POST, request.FILES, instance=profile)

        	if form.is_valid():
        		form.save()

        	login(request, user1)

        	return redirect('office:office-dashboard', pk=office)
    	return redirect('error')


