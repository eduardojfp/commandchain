from django.conf.urls import patterns, include, url
from django.contrib import admin
from chain_of_command import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'chaincommand.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^list_org/',views.Organization_List)
)
