# -*- coding: utf-8 -*-

import warnings
warnings.simplefilter('ignore', UserWarning)

from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy

from feedme import settings
from feedme.context_processors import static_files
from feedme.core.utils import setup_routing


# setup application
app = Flask('feedme')
app.debug = settings.APP_DEBUG
app.secret_key = settings.SEC_KEY

# setup database
app.config['SQLALCHEMY_DATABASE_URI'] = settings.APP_DB_URI
db = SQLAlchemy(app)

# register application views and blueprints
from feedme.urls import routes
setup_routing(app, routes)

# register context processors
app.context_processor(static_files)

# use the debug toolbar if available and debug is enabled
if app.debug:
    try:
        from flaskext.debugtoolbar import DebugToolbarExtension
        debug_tb = DebugToolbarExtension(app)
        app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    except ImportError:
        pass
# setup logging by email if debug is disabled
else:
    import logging
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler(
        settings.MAIL_SERVER,
        settings.MAIL_FROM,
        settings.MAIL_USERS,
        settings.MAIL_SUBJECT
    )
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(logging.Formatter("""
        Message Type:   %(levelname)s
        Location:       %(pathname)s:%(lineno)d
        Module:         %(module)s
        Function:       %(funcName)s
        Time:           %(asctime)s

        Message:
        %(message)s
    """))
    app.logger.addHandler(mail_handler)
