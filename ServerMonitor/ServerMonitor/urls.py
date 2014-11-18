from django.conf.urls import patterns, include, url
from django.contrib import admin
from MonitorAPP.views import *
import xadmin
from xadmin.plugins import xversion
xversion.register_models()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ServerMonitor.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^hello', hello),
    url(r'^xadmin/',include(xadmin.site.urls)),
)
