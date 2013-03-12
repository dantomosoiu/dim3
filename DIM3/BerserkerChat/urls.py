from django.conf.urls import patterns, url, include

from BerserkerChat import views

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

urlpatterns = patterns('',
    url(r'^register/$', views.register, name='register'),
    url(r'^upgrade/$', views.upgrade, name='upgrade'),
    url(r'^myaccount/$', views.myaccount, name='myaccount'),
    url(r'^login/$', views.login, name='login'),
    url(r'^Categories$', views.Categories, name='Categories'),
    url(r'^Recent$', views.Recent, name='Recent'),
    url(r'^chat/', include('chatrooms.urls')),
    url(r'^room/', views.index, name='index'),
    url(r'^$', views.index, name='index')
)
