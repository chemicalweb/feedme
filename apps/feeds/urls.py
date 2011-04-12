from django.conf.urls.defaults import patterns, url

from apps.feeds.models import Post, Feed, Section


urlpatterns = patterns('apps.feeds.views',
    url(r'feed/(\d+)$', 'feed', name='feed'),
    url(r'update$', 'update_all', name='update_all'),
    url(r'read$', 'mark_as_read', name='mark_as_read'),
)

# url patterns for generic views
urlpatterns += patterns('django.views.generic',
    url(r'^$', 'simple.direct_to_template', {
        'template': 'feeds/index.html',
    }, name='index'),

    url(r'section/(?P<object_id>[0-9]+)$', 'list_detail.object_detail', {
        'queryset': Section.objects.all(),
        'template_object_name': 'section',
    }, name='section'),

    url(r'post/(?P<object_id>[0-9]+)$', 'list_detail.object_detail', {
        'queryset': Post.objects.all(),
        'template_object_name': 'post',
    }, name='post'),
)
