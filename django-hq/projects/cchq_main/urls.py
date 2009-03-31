from django.conf.urls.defaults import *
from django.conf.urls import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^$', 'views.homepage'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),
    
    (r'^i18n/$', include('django.conf.urls.i18n')),
    #(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', {}),
    (r'^formreceiver/', include('submitlogger.urls')),
    (r'^modelrelationship/', include('modelrelationship.urls')),
    (r'^xformmanager/', include('xformmanager.urls')),
    (r'^charts/', include('djflot.urls')),
    (r'^organization/', include('organization.urls')),    
    

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
)
