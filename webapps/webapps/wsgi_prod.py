"""
WSGI config for webapps project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webapps.settings.prod")

_application = get_wsgi_application()


def application(environ, start_response):
    os.environ["DATABASE_HOST"] = environ["DATABASE_HOST"]
    os.environ["DATABASE_NAME"] = environ["DATABASE_NAME"]
    os.environ["DATABASE_USER"] = environ["DATABASE_USER"]
    os.environ["DATABASE_PASSWORD"] = environ["DATABASE_PASSWORD"]
    os.environ["DATABASE_PORT"] = environ["DATABASE_PORT"]
    os.environ["SECRET_KEY"] = environ["SECRET_KEY"]
    os.environ["EMAIL_HOST"] = environ["EMAIL_HOST"]
    os.environ["EMAIL_PORT"] = environ["EMAIL_PORT"]
    os.environ["EMAIL_HOST_USER"] = environ["EMAIL_HOST_USER"]
    os.environ["EMAIL_HOST_PASSWORD"] = environ["EMAIL_HOST_PASSWORD"]
    os.environ["DEFAULT_FROM_EMAIL"] = environ["DEFAULT_FROM_EMAIL"]
    return _application(environ, start_response)
