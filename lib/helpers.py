from datetime import datetime
from functools import wraps
from time import mktime

from django.db.utils import IntegrityError
from django.shortcuts import render_to_response
from django.template import RequestContext

import feedparser

from apps.feeds.models import Post


def update_feed(feed):
    """
    Parse a feed and return an iterator of new Post objects
    ready to be saved in database.
    """
    parsed = feedparser.parse(feed.url)

    # update feed title/description if needed
    feed_changed = False
    if hasattr(parsed.feed, 'title') and (feed.title is None):
        feed.title = parsed.feed.title
        feed_changed = True
    if hasattr(parsed.feed, 'description') and (feed.description is None):
        feed.description = parsed.feed.description
        feed_changed = True
    if feed_changed:
        feed.save()

    for entry in parsed.entries:
        try:
            pubdate = entry.get('updated_parsed', None)
            if pubdate is not None:
                pubdate = datetime.fromtimestamp(mktime(pubdate))
            post = Post(
                feed=feed,
                author=feed.get('author', None),
                link=entry.link,
                title=entry.title,
                summary=entry.summary,
                published=pubdate,
                is_read=False,
            )
            yield post
        except IntegrityError:
            continue


class render_to(object):
    """
    Simplify template rendering by decorating view functions.

    Usage:
        @render_to('my_template.html')
        def index(request):
            return {'message': 'Hello World!'}
    """
    def __init__(self, template):
        self.template = template

    def __call__(self, view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            request = args[0]
            context = view(*args, **kwargs)
            return render_to_response(
                self.template,
                context,
                context_instance=RequestContext(request),
            )
        return wrapper
