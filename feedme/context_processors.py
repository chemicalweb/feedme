# -*- coding: utf-8 -*-

def static_files():
    STATIC_PATH = '/static'
    return dict(
        STATIC_PATH = STATIC_PATH,
        CSS_PATH = '%s/css' % STATIC_PATH,
        JS_PATH = '%s/js' % STATIC_PATH,
        MEDIA_PATH = '%s/media' % STATIC_PATH
    )
