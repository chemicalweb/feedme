from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

import apps.aggregator.urls


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(apps.aggregator.urls))
)
