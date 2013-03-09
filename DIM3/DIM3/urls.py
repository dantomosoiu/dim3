from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import os

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^BerserkerChat/', include('BerserkerChat.urls')),
    url(r'^chat/', include('chatrooms.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': ROOT_PATH + '/DIM3/beserkerchat/DIM3/static'}),
    url(r'^google/login/$', 'django_openid_auth.views.login_begin', name='openid-login'),
    url(r'^google/login-complete/$', 'django_openid_auth.views.login_complete', name='openid-complete'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/',}, name='logout'),

    # Examples:
    # url(r'^$', 'DIM3.views.home', name='home'),
    # url(r'^DIM3/', include('DIM3.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('BerserkerChat.urls')),
)

urlpatterns += staticfiles_urlpatterns()