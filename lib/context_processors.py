from django.conf import settings

from apps.feeds.models import Section


def debug_status(request):
    return {
        'DEBUG': settings.DEBUG,
    }

def sections_list(request):
    return {
        'SECTIONS': Section.objects.all(),
    }
