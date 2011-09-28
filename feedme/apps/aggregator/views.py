from django.db import IntegrityError
from django.shortcuts import redirect
from django.views.generic import ListView
from apps.aggregator.models import Section, Feed
from apps.aggregator.utils import get_new_posts


class IndexView(ListView):
    context_object_name = 'sections'
    model = Section
    template_name = 'index.html'


def update(request):
    """Update given feed, if no feed is given, update all feeds."""
    def save(item):
        try:
            item.save()
        except IntegrityError:
            pass
    for feed in Feed.objects.all():
        for new_post in get_new_posts(feed):
            save(new_post)
    return redirect('/')
