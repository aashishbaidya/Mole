from functools import wraps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView as BaseUpdateView, CreateView as BaseCreateView, DeleteView as \
    BaseDeleteView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import PermissionDenied

from office.models import Office


class UpdateView(BaseUpdateView):
    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['scenario'] = _('Edit')
        super(UpdateView, self).get_context_data()
        return context

    def post(self, request, *args, **kwargs):
        response = super(UpdateView, self).post(request, *args, **kwargs)
        if hasattr(response, 'context_data') and not response.context_data.get('form').is_valid():
            messages.warning(request, ('%s %s' % (self.object.__class__._meta.verbose_name.title(),
                                              _('Update Data Not Valid!'))))
        else:

            messages.success(request, ('%s %s' % (self.object.__class__._meta.verbose_name.title(),
                                              _('successfully Updated!'))))
        return response


class DeleteView(BaseDeleteView):
    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = super(DeleteView, self).post(request, *args, **kwargs)
        messages.success(request, ('%s %s' % (self.object.__class__._meta.verbose_name.title(),
                                              _('successfully deleted!'))))
        return response


class CreateView(BaseCreateView):
    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['scenario'] = _('Add')
        return context

    def post(self, request, *args, **kwargs):
        response = super(CreateView, self).post(request, *args, **kwargs)
        if self.object:
            messages.success(request, ('%s %s' % (self.object.__class__._meta.verbose_name.title(),
                                              _('successfully created!'))))
        return response


class OfficeRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.company:
            raise PermissionDenied()
        return super(OfficeRequiredMixin, self).dispatch(request, *args, **kwargs)


class OfficeView(LoginRequiredMixin):
    def form_valid(self, form):
        if self.request.office:
            form.instance.office = self.request.office
        return super(OfficeView, self).form_valid(form)

    def get_queryset(self):
        if self.request.office:
            return super(OfficeView, self).get_queryset().filter(office=self.request.office)
        else:
            return super(OfficeView, self).get_queryset()

    def get_form(self, *args, **kwargs):
        form = super(OfficeView, self).get_form(*args, **kwargs)
        if self.request.office:
            form.office = self.request.office
            if hasattr(form.Meta, 'office_filters'):
                for field in form.Meta.office_filters:
                    form.fields[field].queryset = Office.objects.filter(id=self.request.office.pk)
        return form


USURPERS = {
    'office_head': ['Office Head', 'Admin Assistant', 'Super Admin'],
    'officer': ['Information Officer', 'Office Head', 'Admin Assistant', 'Super Admin'],
    'office': ['Information Officer', 'Office Head',],
    'assistant': ['Admin Assistant', 'Super Admin'],
    'admin': ['Super Admin'],
}


class OfficeHeadMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            if request.role.group.name in USURPERS['office_head']:
                return super(OfficeHeadMixin, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied()


class OfficerMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            if request.role.group.name in USURPERS['officer']:
                return super(OfficerMixin, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied()


class OfficeOnlyMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            if request.role.group.name in USURPERS['office']:
                return super(OfficeOnlyMixin, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied()


class AdminAssistantMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            if request.role.group.name in USURPERS['assistant']:
                return super(AdminAssistantMixin, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied()


class SuperAdminMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            if request.role.group.name in USURPERS['admin']:
                return super(SuperAdminMixin, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied()


def group_required(group_name):
    def _check_group(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated():
                if request.role.group.name in USURPERS.get(group_name, []):
                    return view_func(request, *args, **kwargs)
            raise PermissionDenied()

        return wrapper

    return _check_group


