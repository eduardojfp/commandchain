from chain_of_command.views_org import apply_to_org, delete_org, \
    create_organization, organization_view
from chain_of_command.views_position import create_position, edit_position, position_display

__author__ = 'awhite'
from django.conf.urls import patterns, url
from chain_of_command import views


org_patterns = patterns('',
                        url(r'^(?P<org_id>\d+)/$', organization_view),
                        url(r'^(?P<org_id>\d+)/positions[/]*$',
                            position_display),
                        url(r'^(?P<org_id>\d+)/positions/(?P<pos_id>\d+)/edit',
                            edit_position),
                        url(r'^(?P<org_id>\d+)/positions/create',
                            create_position),
                        url(r'^(?P<org_id>\d+)/delete', delete_org),
                        url(r'^create/', create_organization),
                        url(r'^apply/', apply_to_org),
)