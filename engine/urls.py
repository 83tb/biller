from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('',

    url(r'^list', 'engine.views.connections'),
    url(r'^engine$', 'engine.views.rpc_handler'),    


    )

