from .base import *
import os
import dj_database_url

# -- HEROKU NEEDS DEBUG = TRUE --
# DEBUG = False

# # SECURITY WARNING: define the correct hosts in production!
# ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(";")

DEBUG = False
ALLOWED_HOSTS = ["*"]

# --Heroku things--
COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    "compressor.filters.css_default.CssAbsoluteFilter",
    "compressor.filters.cssmin.CSSMinFilter",
]
COMPRESS_CSS_HASHING_METHOD = "content"
PRODUCTION = os.environ.get("DATABASE_URL")
if PRODUCTION:
    DATABASES["default"] = dj_database_url.config()
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

try:
    from .local import *
except ImportError:
    pass
