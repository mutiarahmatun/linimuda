import os
from .base import *

DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(";")

try:
    from .local import *
except ImportError:
    pass
