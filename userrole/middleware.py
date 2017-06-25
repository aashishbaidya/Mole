from userrole.models import UserRole as Role


def clear_roles(request):
    request.__class__.role = None
    request.__class__.office = None
    request.__class__.ad = None
    request.__class__.group = None
    request.__class__.roles = []
    request.__class__.is_super_admin = False
    return request


class RoleMiddleware(object):
    def process_request(self, request):

        if request.META.get('HTTP_AUTHORIZATION'):
            pass

        if not request.user.is_anonymous():

            role = None
            if request.session.get('role'):
                try:
                    role = Role.objects.select_related('group', 'office').get(pk=request.session.get('role'),
                                                                                     user=request.user)
                except Role.DoesNotExist:
                    pass

            if not role:
                roles = Role.get_active_roles(request.user)
                if roles:
                    role = roles[0]
                    request.session['role'] = role.id
            if role:
                request.__class__.role = role
                request.__class__.office = role.office
                request.__class__.group = role.group
                request.__class__.roles = Role.get_active_roles(request.user)
                request.__class__.is_super_admin = request.group.name == 'Super Admin'
            else:
                clear_roles(request)
        else:
            clear_roles(request)
