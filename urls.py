from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.defaults import *

from django.views.generic.simple import direct_to_template

from django.contrib import admin


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^biller/', include('biller.engine.urls')),
    url(r'^accounts/', include('registration.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^$', 'engine.views.connections')
    url(r'^$', direct_to_template, { 'template': 'index.html' }, 'index')

)
