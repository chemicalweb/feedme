from django.core.cache import cache
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from apps.feeds.forms import MarkAsRead
from apps.feeds.models import Feed, Post

from datetime import datetime
from time import mktime

import feedparser

from lib.helpers import render_to


@render_to("feeds/feed.html")
def feed(request, feed_id):
    f = get_object_or_404(Feed, pk=feed_id)
    post_list = cache.get("feed#%s" % feed_id)
    if post_list is None:
        post_list = f.post_set.all()
        cache.set("feed#%s" % feed_id, post_list, 600)

    paginator = Paginator(post_list, 5)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        posts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)
    return dict(
        feed=f,
        posts=posts
    )

def mark_as_read(request):
    if request.method == 'POST':
        form = MarkAsRead(request.POST)
        if form.is_valid():
            post = get_object_or_404(Post, pk=form.cleaned_data['post_id'])
            if not post.is_read:
                post.is_read = True
                post.save()
    return HttpResponseRedirect('/')

def update_all(request):
    cache.clear()
    for feed in Feed.objects.all():
        parsed = feedparser.parse(feed.url)
        if parsed.feed.description and (feed.description is None):
            feed.description = parsed.feed.description
            feed.save()
        for entry in parsed.entries:
            try:
                if hasattr(entry, 'updated_parsed'):
                    pubdate = datetime.fromtimestamp(mktime(entry.updated_parsed))
                else:
                    pubdate = None
                post = Post(
                    feed=feed,
                    link=entry.link,
                    title=entry.title,
                    summary=entry.summary,
                    published=pubdate,
                    is_read=False,
                )
                post.save()
            except IntegrityError:
                pass
    return HttpResponseRedirect('/')

def update_feed(request, feed_id):
    return HttpResponseRedirect('/')
