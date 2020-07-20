import os
from .base import *

# -- HEROKU NEEDS DEBUG = TRUE --
# DEBUG = False

# # SECURITY WARNING: define the correct hosts in production!
# ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(";")

DEBUG = True
ALLOWED_HOSTS = []

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

try:
    from .local import *
except ImportError:
    pass
