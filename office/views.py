# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView
from django.shortcuts import render, get_object_or_404

from reports.models import KaryaKram
from .models import Office, ProjectDetail, MunicipalityDetail, District
from .forms import OfficeForm, UserForm, MunicipalityDetailForm, ProjectDetailForm, OfficeEditForm

from userrole.mixins import CreateView, UpdateView, DeleteView, OfficerMixin, AdminAssistantMixin

from django.views.generic import View
from django.shortcuts import render, redirect


from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from .tokens import account_activation_token
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.core.urlresolvers import reverse
from userrole.models import UserRole

class OfficeView(object):
    model = Office
    success_url = reverse_lazy('office:office-list')
    form_class = OfficeForm

class ProjectView(object):
    model = ProjectDetail
    success_url = reverse_lazy('office:office-list')
    form_class = ProjectDetailForm

class MunicipalityView(object):
    model = MunicipalityDetail
    success_url = reverse_lazy('office:office-list')
    form_class = MunicipalityDetailForm

class OfficeUserView(LoginRequiredMixin, TemplateView):
    template_name = 'office/users.html'

    def get_context_data(self, **kwargs):
        context = super(OfficeUserView, self).get_context_data(**kwargs)

        context['office'] = kwargs.get('pk')
        context['head'] = UserRole.get_office_user('Office Head', kwargs.get('pk'))
        context['assistant'] = UserRole.get_office_user('Information Officer', kwargs.get('pk'))
        return context

class OfficeKaryakram(LoginRequiredMixin, OfficeView, DetailView):
    template_name = 'reports/karyakram.html'

class OfficeKaryakramBudget(LoginRequiredMixin, OfficeView, DetailView):
    template_name = 'reports/karyakram_budget.html'


class OfficeDetailView(LoginRequiredMixin, OfficeView, DetailView):
    pass


class OfficeListView(LoginRequiredMixin, AdminAssistantMixin, OfficeView, ListView):
    context_object_name = 'all_offices'
    pass


class OfficeCreateView(LoginRequiredMixin, AdminAssistantMixin, OfficeView, CreateView):
    def from_valid(self, form):
        self.object = form.save()

    
    def get_success_url(self):
        
        if self.object.is_municipality == True:
            return reverse('office:office-add-municipilaty',args=(self.object.id,))    
        elif self.object.is_project == True:
            return reverse('office:office-add-project',args=(self.object.id,))
        else:
            return reverse_lazy('office:office-list')

class OfficeUpdateView(LoginRequiredMixin, OfficerMixin, OfficeView, UpdateView):
    template_name = 'office/office-update.html'
    form_class = OfficeEditForm


class OfficeDeleteView(LoginRequiredMixin, AdminAssistantMixin, OfficeView, DeleteView):
    pass

class OfficeAddMunicipilaty(LoginRequiredMixin, AdminAssistantMixin, OfficeView, View):
    def get(self, request, pk):
        form_type = MunicipalityDetailForm()
        return render(request, 'office/add_office_detail.html', {'form': form_type, 'id':pk})

    def post(self, request, *args, **kwargs):
            office_id = request.POST.get('office_id')
            details =MunicipalityDetailForm(request.POST)

            if details.is_valid():
                    detail =  details.save(commit=False)
                    detail.office = Office.objects.get(id=office_id)
                    detail.save()


            return redirect('office:office-dashboard', pk=office_id)


class ProjectUpdate(LoginRequiredMixin, OfficerMixin, ProjectView, UpdateView): 
    template_name = 'office/update-project-municipality.html'
     

class MunicipalityUpdate(LoginRequiredMixin, OfficerMixin, MunicipalityView, View):
    template_name = 'office/update-project-municipality.html'

class OfficeAddProject(LoginRequiredMixin, AdminAssistantMixin, OfficeView, View):
    def get(self, request, pk):
        form_type = ProjectDetailForm()
        return render(request, 'office/add_office_detail.html', {'form': form_type, 'id':pk})

    def post(self, request, *args, **kwargs):
            office_id = request.POST.get('office_id')
            details =ProjectDetailForm(request.POST)

            if details.is_valid():
                    detail =  details.save(commit=False)
                    detail.office = Office.objects.get(id=office_id)
                    detail.save()
                    #return redirect('question_detail', pk=question.pk)
            return redirect('office:office-dashboard', pk=office_id)



class OfficeAddOfficeHeadView(LoginRequiredMixin, AdminAssistantMixin, OfficeView, View):
    def get(self, request, pk):
        user = UserForm()
        return render(request, 'office/addnewuser.html', {'form': user, 'office_id': pk, 'role':'Office Head'})

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        role= request.POST.get('role')
        office = request.POST.get('office')
        if form.is_valid:
            user = form.save(commit=False)
            user.is_active = False
            user.set_unusable_password()
            user.save()
            user.profile.office = Office.objects.get(id=request.POST.get('office'))
            user.save()

            grp = Group.objects.get(name=role)
            grp.user_set.add(user)

            #email sending part
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('office/accountconfirm.html',
            {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),})
            user.email_user(subject, message)
            return redirect('office:office-dashboard', pk=office)

class OfficeAddInfoofficerView(LoginRequiredMixin, AdminAssistantMixin, OfficeView, View):
    def get(self, request, pk):
        user = UserForm()
        return render(request, 'office/addnewuser.html', {'form': user, 'office_id': pk, 'role':'Information Officer'})

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        role= request.POST.get('role')
        office = request.POST.get('office')
        if form.is_valid:
            user = form.save(commit=False)
            user.is_active = False
            user.set_unusable_password()
            user.save()
            user.profile.office = Office.objects.get(id=request.POST.get('office'))
            user.save()

            grp = Group.objects.get(name=role)
            grp.user_set.add(user)

            #email sending part
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('office/accountconfirm.html',
            {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),})
            user.email_user(subject, message)
            return redirect('office:office-dashboard', pk=office)


class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = "office/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['offices'] = Office.objects.all()
        context['projects'] = Office.objects.filter(is_project=True)
        context['submission_count'] = 0
        context['offices_count'] = Office.objects.all().count()
        context['users_count'] = User.objects.all().count()

        return context



class OfficeDashboard(LoginRequiredMixin, TemplateView):

    template_name = "office/office_dashboard.html"
    def get_context_data(self, **kwargs):
        context = super(OfficeDashboard, self).get_context_data(**kwargs)
        office = Office.objects.get(pk=kwargs.get('pk'))

        context['office'] = office
        context['karyakrams'] = KaryaKram.objects.filter(office=office)
        return context


class OfficeDashboardSubmit(LoginRequiredMixin, TemplateView):

    template_name = "office/office_dashboard_submit.html"


class DistrictDashboard(LoginRequiredMixin, TemplateView):

    template_name = "office/district_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DistrictDashboard, self).get_context_data(**kwargs)
        district = District.objects.get(pk=kwargs.get('pk'))

        context['district'] = district
        context['offices'] = Office.objects.filter(district=district)
        return context
