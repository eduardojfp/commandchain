__author__ = 'awhite'
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login
from chain_of_command import views
from django.conf.urls.static import static
from chaincommand import settings

org_patterns = patterns('',
                        url(r'^(?P<org_id>\d+)/$', views.organization_view),
                        url(r'^(?P<org_id>\d+)/positions[/]*$',
                            views.position_display),
                        url(r'^(?P<org_id>\d+)/positions/(?P<pos_id>\d+)/edit',
                            views.edit_position),
                        url(r'^(?P<org_id>\d+)/positions/create',
                            views.create_position),
                        url(r'^(?P<org_id>\d+)/delete', views.delete_org),
                        url(r'^create/', views.create_organization),
                        url(r'^apply/', views.apply_to_org)
)