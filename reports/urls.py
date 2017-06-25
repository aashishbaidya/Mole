from django.conf.urls import url


from .views import KaryakramCreateView, KaryakramUpdateView, LakxyaCreateView, PragatiCreateView, KaryakramListView, \
    ReportView

app_name = 'reports'

urlpatterns = [
    url(r'^karyakram/list/(?P<office>[0-9]+)/$', KaryakramListView.as_view(), name='karyakram-list'),
    url(r'^karyakram/create/(?P<office>[0-9]+)/$', KaryakramCreateView.as_view(), name='karyakram-add'),
    url(r'^list/(?P<office>[0-9]+)/(?P<awadhi>[0-9]+)/$', ReportView.as_view(), name='reports'),
    url(r'^karyakram/update/(?P<office>[0-9]+)/(?P<pk>[0-9]+)/$', KaryakramUpdateView.as_view(), name='karyakram-update'),
    url(r'^karyakram/addlaksya/(?P<office>[0-9]+)/(?P<karyakram_id>[0-9]+)/(?P<awadhi>[0-9]+)/$', LakxyaCreateView.as_view(), name='add-laksya'),
    url(r'^karyakram/addpragati/(?P<office>[0-9]+)/(?P<karyakram_id>[0-9]+)/(?P<awadhi>[0-9]+)/$', PragatiCreateView.as_view(), name='add-pragati'),
        ]