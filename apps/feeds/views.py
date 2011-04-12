from django.core.cache import cache
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from apps.feeds.forms import MarkAsRead
from apps.feeds.models import Feed, Post

from lib.helpers import render_to, update_feed


@render_to("feeds/feed.html")
def feed(request, feed_id):
    """Display a feed and its posts."""
    f = get_object_or_404(Feed, pk=feed_id)
    # cache posts
    post_list = cache.get("feed#%s" % feed_id)
    if post_list is None:
        post_list = f.post_set.all()
        cache.set("feed#%s" % feed_id, post_list, 600)
    # paginate entries
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
    """Mark a post as read."""
    if request.method == 'POST':
        form = MarkAsRead(request.POST)
        if form.is_valid():
            post = get_object_or_404(Post, pk=form.cleaned_data['post_id'])
            if not post.is_read:
                post.is_read = True
                post.save()
    return HttpResponseRedirect('/')

def update_all(request):
    """Get new posts for all the feeds."""
    cache.clear()
    for feed in Feed.objects.all():
        for post in update_feed(feed):
            post.save()
    return HttpResponseRedirect('/')

def update_feed(request, feed_id):
    """Get new posts for given feed."""
    feed = get_object_or_404(Feed, pk=feed_id)
    for post in update_feed(feed):
        post.save()
    return HttpResponseRedirect('/')
