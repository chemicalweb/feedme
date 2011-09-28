from datetime import datetime
from time import mktime

from apps.aggregator.models import Post

import feedparser


def get_new_posts(feed):
    """
    Returns an iterator of new Post objects for given `feed`.
    """
    parsed = feedparser.parse(feed.url)

    feed_edited = False
    if (feed.title == feed.url) and ('title' in parsed.feed):
        # title was previously set to feed url but it is
        # now available in the parsed information, update it.
        feed.title = parsed.feed.title
        feed_edited = True
    if not feed.title:
        # title was never set, get it from the parsed informations if
        # available, otherwise set it to the feed url.
        feed.title = parsed.feed.get('title', feed.url)
        feed_edited = True
    if (not feed.description) and ('description' in parsed.feed):
        feed.description = parsed.feed.description
        feed_edited = True
    if feed_edited:
        feed.save()

    for new_post in parsed.entries:
        pubdate = new_post.get('updated_parsed')
        pubdate = datetime.fromtimestamp(mktime(pubdate)) if (
            pubdate is None
            ) else datetime.now()
        post = Post(
            feed = feed,
            author = new_post.get('author', None),
            link = new_post.link,
            title = new_post.title,
            summary = new_post.description,
            published = pubdate
        )
        yield post
