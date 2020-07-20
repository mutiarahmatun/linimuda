from __future__ import absolute_import, unicode_literals
from .base import *
import os
import dj_database_url

# -- HEROKU NEEDS DEBUG = TRUE --
# DEBUG = False

# # SECURITY WARNING: define the correct hosts in production!
# ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(";")

DEBUG = True
ALLOWED_HOSTS = ["*"]

# Heroku postgresql
PRODUCTION = os.environ.get("DATABASE_URL")
if PRODUCTION:
    print("This is production")
    DATABASES = {}
    DATABASES["default"] = dj_database_url.config()
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

try:
    from .local import *
except ImportError:
    pass
