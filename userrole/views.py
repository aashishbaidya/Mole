from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView

from userrole.forms import UserRoleForm
from userrole.mixins import LoginRequiredMixin, SuperAdminMixin, CreateView, UpdateView, DeleteView
from userrole.models import UserRole as Role, UserRole


def set_role(request, pk):
    role = Role.objects.get(pk=pk, user=request.user)
    if role:
        request.session['role'] = role.pk
    return redirect(request.META.get('HTTP_REFERER', '/'))


class UserRoleView(object):
    model = UserRole
    success_url = reverse_lazy('role:user-role-list')
    form_class = UserRoleForm         


class UserRoleListView(LoginRequiredMixin, SuperAdminMixin, UserRoleView, ListView):
    pass


class UserRoleCreateView(LoginRequiredMixin, SuperAdminMixin, UserRoleView, CreateView):
    pass


class UserRoleUpdateView(LoginRequiredMixin, SuperAdminMixin, UserRoleView, UpdateView):
    pass


class UserRoleDeleteView(LoginRequiredMixin, SuperAdminMixin, UserRoleView, DeleteView):
    pass

