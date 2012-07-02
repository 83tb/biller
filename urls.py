from django.conf.urls.defaults import patterns, include, url


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^biller/', include('biller.engine.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
