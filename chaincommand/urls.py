from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login
from chain_of_command import views, urls as hello
from django.conf.urls.static import static
from chaincommand import settings

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'chaincommand.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^list_org/', views.Organization_List),
                       # url(r'^org/(?P<org_id>\d+)/$', views.OrganizationView,
                       # name='Org_detail'),
                       # url(r'^org/(?P<org_id>\d+)/positions',
                       #     views.position_display, name='position_display'),
                       url(r'^user/$', views.user_page,
                           name="User_page"),
                       url(r'^logout/$', views.logout_page, name="logout page"),
                       url(r'^login/$', views.login,
                           name="login"),
                       # url(r'^org/create/$', views.create_organization,
                       #    name='create org'),
                       url(r'^post/(?P<member_id>\d+)/create',
                           views.create_post,
                           name='create post'),
                       url(r'^post/(?P<post_id>\d+)/view$', views.view_post,
                           name='view post'),
                       (r'^ckeditor/', include('ckeditor.urls')),
                       url(r'^post/(?P<post_id>\d+)/edit$', views.edit_post,
                           name='edit post'),
                       url(r'^org/', include(hello.org_patterns))
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)