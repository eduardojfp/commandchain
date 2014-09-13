from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login
from chain_of_command import views

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'chaincommand.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^list_org/', views.Organization_List),
                       url(r'^org/(?P<org_id>\d+)/$', views.OrganizationView,
                           name='Org_detail'),
                       url(r'^org/(?P<org_id>\d+)/positions',
                           views.position_display, name='position_display'),
                       url(r'^user/$', views.user_page,
                           name="User_page"),
                       url(r'^logout/$', views.logout_page, name="logout page"),
                       url(r'^login/$', views.login, name="login")
)
