# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, ListView

from office.models import Office
from reports.forms import KaryakramForm, LakxyaForm, PragatiForm
from reports.models import KaryaKram, Lakxya, Pragati
from userrole.mixins import CreateView, UpdateView, OfficeView, OfficerMixin
from django.core.urlresolvers import reverse
from django.db.models import Prefetch


class KaryakramView(object):
    model = KaryaKram
    form_class = KaryakramForm

class LakxyaView(object):
    model = Lakxya
    form_class = LakxyaForm

class PragatiView(object):
    model = Pragati
    form_class = PragatiForm



class KaryakramCreateView(OfficeView, KaryakramView, CreateView):

    def get(self, request, *args, **kwargs):
        office = self.kwargs['office']
        return render(request, 'reports/karyakram_form.html', {'office': office},)


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.office = Office(pk=self.kwargs.get('office'))
        self.object.save()
        return redirect(reverse('reports:add-laksya',args=(self.object.office.id, self.object.id, 0)))

class KaryakramUpdateView(OfficeView, KaryakramView, UpdateView):
    pass


class KaryakramListView(OfficeView, KaryakramView, OfficerMixin, ListView):
    def get_context_data(self, **kwargs):
        data = super(KaryakramListView, self).get_context_data(**kwargs)
        data['office'] = self.kwargs.get('office')
        return data

    def get_queryset(self):
        # filter fiscal year == office.settings.fiscal year
        return super(KaryakramListView, self).get_queryset().filter(office__id=self.kwargs.get('office'))

class LakxyaCreateView(OfficeView, LakxyaView, FormView):
    template_name = 'reports/lakxya_form.html'


    def get(self, request, *args, **kwargs):
        awadhi = self.kwargs['awadhi']
        karyakram_id = self.kwargs['karyakram_id']
        karyakram = KaryaKram.objects.get(pk=karyakram_id)
        laxya, created = Lakxya.objects.get_or_create(karyakram=karyakram, fiscal_year_id=1, awadhi=awadhi)
        form = LakxyaForm(instance=laxya)
        return render(request, 'reports/lakxya_form.html', {'form': form,'awadhi': awadhi, 'karyakram':karyakram},)


    def form_valid(self, form):
        lakxya = Lakxya.objects.get(pk=form.data.get('lakxya'))
        lakxya.paridam = form.cleaned_data['paridam']
        lakxya.var = form.cleaned_data['var']
        lakxya.budget = form.cleaned_data['budget']
        lakxya.save()
        # correct url to redirect after lakxya save and fill pragati
        

        if lakxya.awadhi == 0:
            return redirect(reverse('reports:add-laksya',args=(lakxya.karyakram.office.id, lakxya.karyakram.id, 1)))
        else:
            return redirect(reverse('office:office-dashboard',args=(lakxya.karyakram.office.id,)))

class PragatiCreateView(OfficeView, PragatiView, CreateView):
    def get(self, request, *args,  **kwargs):
        awadhi = self.kwargs['awadhi']
        karyakram_id = self.kwargs['karyakram_id']
        karyakram = KaryaKram.objects.get(pk=karyakram_id)
        pragati, created = Pragati.objects.get_or_create(karyakram=karyakram, fiscal_year_id=1, awadhi=awadhi)
        form = PragatiForm(instance=pragati)
        return render(request, 'reports/pragati_form.html', {'form': form,'awadhi': awadhi, 'karyakram':karyakram},)


    def form_valid(self, form):
        pragati = Pragati.objects.get(pk=form.data.get('pragati'))
        pragati.paridam = form.cleaned_data['paridam']
        pragati.var = form.cleaned_data['var']
        pragati.budget = form.cleaned_data['budget']
        pragati.save()
        # correct url to redirect after lakxya save and fill pragati
        if pragati.awadhi == 1:
            return redirect(reverse('reports:add-laksya',args=(pragati.karyakram.office.id, pragati.karyakram.id, 2)))
        else:
            return redirect(reverse('office:office-dashboard',args=(pragati.karyakram.office.id,)))


class ReportView(OfficeView, OfficerMixin, KaryakramView, ListView):
    template_name = 'reports/reports.html'

    def get_context_data(self, **kwargs):
        data = super(ReportView, self).get_context_data(**kwargs)
        data['office'] = self.kwargs.get('office')
        data['awadhi'] = self.kwargs.get('awadhi')
        return data

    def get_queryset(self):
        # filter fiscal year == office.settings.fiscal year
        qs =  KaryaKram.objects.filter(office__id=self.kwargs.get("office"), lakxya__awadhi=0, pragati__awadhi=1).\
            prefetch_related("lakxya", "pragati")
        return qs


class KaryakramControlList(OfficeView, OfficerMixin, KaryakramView, ListView):
    template_name = 'reports/karyakram_control.html'

    def get_context_data(self, **kwargs):
        data = super(KaryakramControlList, self).get_context_data(**kwargs)
        data['office'] = self.kwargs.get('office')
        data['awadhi'] = self.kwargs.get('awadhi')
        return data

    def get_queryset(self):
        qs = KaryaKram.objects.filter(office__id=self.kwargs.get("office"), karyakram__isnull=True).prefetch_related(Prefetch("parent", to_attr='childs'))

        return qs

class FirstControlList(OfficeView, OfficerMixin, KaryakramView, ListView):

    def get(self, request, *args, **kwargs):
        office = self.kwargs['office']
        return render(request, 'reports/First_control.html', {'office': office}, )


class SecondControlList(OfficeView, OfficerMixin, KaryakramView, ListView):
    def get(self, request, *args, **kwargs):
        office = self.kwargs['office']
        return render(request, 'reports/second_control.html', {'office': office}, )

#only for design implementation
class FirstControlListEdit(OfficeView, OfficerMixin, KaryakramView, ListView):
    def get(self, request, *args, **kwargs):
        office = self.kwargs['office']
        return render(request, 'reports/first_controllist_edit.html', {'office': office}, )


class SecondControlListEdit(OfficeView, OfficerMixin, KaryakramView, ListView):
    def get(self, request, *args, **kwargs):
        office = self.kwargs['office']
        return render(request, 'reports/second_controllist_edit.html', {'office': office}, )


class SecondControlListBudget(OfficeView, OfficerMixin, KaryakramView, ListView):
    def get(self, request, *args, **kwargs):
        office = self.kwargs['office']
        return render(request, 'reports/budget.html', {'office': office}, )

