from django.conf.urls.defaults import patterns, url
from apps.aggregator.views import IndexView


urlpatterns = patterns('apps.aggregator.views',
    url(r'update/$', 'update'),
    url(r'/?$', IndexView.as_view(), name='index'),
)
