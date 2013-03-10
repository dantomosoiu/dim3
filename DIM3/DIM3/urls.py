from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import os

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': ROOT_PATH + '/DIM3/static'}),
    url(r'^google/login/$', 'django_openid_auth.views.login_begin', name='openid-login'),
    url(r'^google/login-complete/$', 'django_openid_auth.views.login_complete', name='openid-complete'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/',}, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('BerserkerChat.urls')),
    url(r'^', include('chatrooms.urls')),
)

urlpatterns += staticfiles_urlpatterns()