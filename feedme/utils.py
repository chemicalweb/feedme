from functools import wraps

from django.shortcuts import render_to_response
from django.template import RequestContext


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
                context_instance=RequestContext(request)
            )
        return wrapper
