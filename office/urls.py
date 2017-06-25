from django.conf.urls import url


from office.views import  OfficeAddMunicipilaty, OfficeAddProject, ProjectUpdate, MunicipalityUpdate

app_name = 'office'

from office.views import OfficeCreateView, OfficeListView, OfficeUpdateView, OfficeDeleteView, DashboardView,\
    OfficeAddOfficeHeadView, OfficeAddInfoofficerView, OfficeDashboard, DistrictDashboard, OfficeKaryakramList



urlpatterns = [

    url(r'^office/create/$', OfficeCreateView.as_view(), name='office-add'),
    url(r'^office/dashboard/(?P<pk>[0-9]+)/$', OfficeDashboard.as_view(), name='office-dashboard'),
    url(r'^district/dashbaord/(?P<pk>[0-9]+)/$', DistrictDashboard.as_view(), name='district-dashboard'),
    url(r'^office/dashboard/(?P<pk>[0-9]+)/karyakramlist/$', OfficeKaryakramList.as_view(), name='office-karyakram-list'),
    url(r'^office/update/(?P<pk>[0-9]+)/$', OfficeUpdateView.as_view(), name='office-update'),
    url(r'^office/delete/(?P<pk>[0-9]+)/$', OfficeDeleteView.as_view(), name='office-delete'),
    url(r'^office/list/$', OfficeListView.as_view(), name='office-list'),
    url(r'^office/(?P<pk>[0-9]+)/adduser/addofficehead/$', OfficeAddOfficeHeadView.as_view(), name='office-add-office-head'),
    url(r'^office/(?P<pk>[0-9]+)/adduser/addinfoofficer/$', OfficeAddInfoofficerView.as_view(), name='office-add-info-officer'),
    #url(r'^office/(?P<pk>[0-9]+)/addtype/$', OfficeAddUserView.as_view(), name='office-addtype'),
    url(r'^office/(?P<pk>[0-9]+)/addmunicipality/$', OfficeAddMunicipilaty.as_view(), name='office-add-municipilaty'),
    url(r'^office/(?P<pk>[0-9]+)/addproject/$', OfficeAddProject.as_view(), name='office-add-project'),
    url(r'^office/(?P<pk>[0-9]+)/updateproject/$', ProjectUpdate.as_view(), name='office-update-project'),
    url(r'^office/(?P<pk>[0-9]+)/updatemunicipality/$', MunicipalityUpdate.as_view(), name='office-update-municipality'),
    url(r'', DashboardView.as_view(), name='dashboard'),

        ]
