import os
import dj_database_url
from .base import *

# -- HEROKU NEEDS DEBUG = TRUE --
# DEBUG = False

# # SECURITY WARNING: define the correct hosts in production!
# ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(";")

DEBUG = True
ALLOWED_HOSTS = ["*"]

# Heroku postgresql
PRODUCTION = os.environ.get("DATABASE_URL")
if PRODUCTION:
    DATABASES = {}
    DATABASES["default"] = dj_database_url.config(conn_max_age=600)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

try:
    from .local import *
except ImportError:
    pass
