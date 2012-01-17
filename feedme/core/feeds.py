# -*- coding: utf-8 -*-

import feedparser
from datetime import datetime
from time import mktime


def parse_feed(feed_url):
    posts = []
    feed  = feedparser.parse(feed_url)
    feed_infos = dict(
        title=feed.channel.title,
        description=feed.channel.description,
        url=feed.channel.link
    )
    for entry in feed.entries:
        post = dict(
            author=entry.get('author', None),
            url=entry.link,
            title=entry.title,
            summary=entry.summary,
            published=datetime.fromtimestamp(mktime(entry.updated_parsed))
        )
        posts.append(post)
    return feed_infos, posts
