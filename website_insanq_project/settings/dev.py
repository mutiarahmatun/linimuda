from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "tbenf5(vmr1c60k)p#u9pbc_iv4l%o1ck6xx#4mq3$l(_-6pda"

ALLOWED_HOSTS = ["*"]

WAGTAIL_CACHE = False

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = "/tmp/app-messages"

try:
    from .local_settings import *  # noqa
except ImportError:
    pass
