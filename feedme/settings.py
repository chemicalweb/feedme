# -*- coding: utf-8 -*-

#############################
# FeedMe Configuration File #
#############################

######################
# Application Settings
#
# switch to False to have errors sent by email (see below for email settings)
APP_DEBUG = True
# database connection URI (see SQLAlchemy documentation for URI format details)
APP_DB_URI = 'sqlite:///feedme.sqlite'
#
#######################

########################
# Email Logging Settings
#
# email addresses to which logged errors should be sent
MAIL_USERS = ['root@localhost']
# SMTP server to use to send emails
MAIL_SERVER = '127.0.0.1'
# "from" address to use in sent emails
MAIL_FROM = 'feedme-error@localhost'
# subject to use in sent emails
MAIL_SUBJECT = 'FeedMe Error Report'
#
########################

###################
# Security Settings
#
# secret key used to encrypt sessions data
SEC_KEY = 'DuMmY sEcReT kEy'
# security level to use for sessions protection (can be 'basic' or 'strong')
SEC_LEVEL = 'strong'
# message to display when a user requests a page without being allowed to access it
SEC_LOGIN_MSG = u'You need to be logged in to access this page'
# message to display when a session needs to be refreshed
SEC_REFRESH_MSG = u'For your security, please re-authenticate'
#
###################

try:
    from .local_settings import *
except ImportError:
    pass
