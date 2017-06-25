from django.conf.urls import url

from userrole.views import set_role

urlpatterns = [
    url(r'^set-role/(?P<pk>[0-9]+)/$', set_role, name='set_role'),
        ]