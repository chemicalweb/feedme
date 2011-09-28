from django.db.models import (
    Model,
    ForeignKey,
    BooleanField,
    CharField,
    DateTimeField,
    TextField,
    URLField,
)


class Section(Model):
    name = CharField(max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Feed(Model):
    section = ForeignKey(Section, related_name='feeds')
    title = CharField(max_length=50, blank=True, null=True)
    description = CharField(max_length=150, blank=True, null=True)
    url = URLField(unique=True)
    favicon = URLField(blank=True, null=True)
    last_update = DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['section__name', 'title']


class Post(Model):
    feed = ForeignKey(Feed, to_field='url', related_name='posts')
    is_read = BooleanField(default=False)
    author = CharField(max_length=250, default='Unknown Author', blank=True, null=True)
    link = URLField(unique=True, verify_exists=False)
    title = CharField(max_length=250)
    summary = TextField()
    published = DateTimeField()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-published', 'feed__title', 'title', 'is_read']
