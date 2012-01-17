# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declared_attr

from feedme import db


class AutoInitModelMixin(object):
    """
    Mixin for populating models' columns automatically (no need to
    define an __init__ method) and set the default value if any.
    Also sets the model's id and __tablename__ automatically.
    """
    id = db.Column(db.Integer, primary_key=True)

    # use the lowercased class name as the __tablename__
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __init__(self, *args, **kwargs):
        for attr in (a for a in dir(self) if not a.startswith('_')):
            attr_obj = getattr(self, attr)
            if isinstance(attr_obj, db.Column):
                if attr in kwargs:
                    setattr(self, attr, kwargs[attr])
                else:
                    if hasattr(attr_obj, 'default'):
                        setattr(self, attr, attr_obj.default)


class Section(db.Model, AutoInitModelMixin):
    name = db.Column(db.String(50))
    feeds = db.relationship('Feed', backref='section', lazy='dynamic')


class Feed(db.Model):
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    title = db.Column(db.String(50), nullable=True)
    description = db.Column(db.String(200), nullable=True)
    url = db.Column(db.String(200), unique=True)
    favicon = db.Column(db.String(200), nullable=True)
    last_update = db.Column(db.DateTime)
    posts = db.relationship('Post', backref='feed', lazy='dynamic')


class Post(db.Model):
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id'))
    is_read = db.Column(db.Bool, default=False)
    author = db.Column(db.String(200), default='Unknown Author')
    url = db.Column(db.String(200), unique=True)
    title = db.Column(db.String(200))
    summary = db.Column(db.Text)
    published = db.Column(db.DateTime)
