from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

# Add your site's domain name(s) here.
ALLOWED_HOSTS = ["*"]
# ALLOWED_HOSTS = ["www.insanq.co.id"]

# To send email from the server, we recommend django_sendmail_backend
# Or specify your own email backend such as an SMTP server.
# https://docs.djangoproject.com/en/3.0/ref/settings/#email-backend


EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = "/tmp/app-messages"
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST:  'localhost'
# EMAIL_PORT: 25
# EMAIL_HOST_USER: (Empty string)
# EMAIL_HOST_PASSWORD: (Empty string)
# -- Default email address used to send messages from the website. ==
# DEFAULT_FROM_EMAIL = "Insanq <info@insanq.co.id>"

# A list of people who get error notifications.
ADMINS = [
    ("Administrator", "admin@insanq.co.id"),
]

# A list in the same format as ADMINS that specifies who should get broken link
# (404) notifications when BrokenLinkEmailsMiddleware is enabled.
MANAGERS = ADMINS

# Email address used to send error messages to ADMINS.
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'HOST': 'localhost',
#         'NAME': 'website_insanq_project',
#         'USER': 'website_insanq_project',
#         'PASSWORD': '',
#         # If using SSL to connect to a cloud mysql database, spedify the CA as so.
#         'OPTIONS': { 'ssl': { 'ca': '/path/to/certificate-authority.pem' } },
#     }
# }

# Use template caching to speed up wagtail admin and front-end.
# Requires reloading web server to pick up template changes.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
            ],
            "loaders": [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                    ],
                ),
            ],
        },
    },
]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": os.path.join(BASE_DIR, "cache"),  # noqa
        "KEY_PREFIX": "coderedcms",
        "TIMEOUT": 14400,  # in seconds
    }
}

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
SECURE_SSL_REDIRECT = True

try:
    from .local_settings import *  # noqa
except ImportError:
    pass
