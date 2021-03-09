"""
Django settings for webapps project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.utils.translation import gettext_lazy as _

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    # This project
    "webapps.apps.home",
    "webapps.apps.article",
    "webapps.apps.contact_us",
    "webapps.apps.event",
    "webapps.apps.information",
    "webapps.apps.video",
    "webapps.apps.override_dashboard_admin",
    "webapps.apps.website",
    # CodeRed
    "coderedcms",
    "bootstrap4",
    "modelcluster",
    "taggit",
    "wagtailfontawesome",
    "wagtailcache",
    # "wagtailimportexport",
    # Wagtail
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.core",
    "wagtail.contrib.settings",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.table_block",
    "wagtail.admin",
    # Django
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    # Compressor
    "compressor",
    # Django Allauth Required
    "django.contrib.messages",
    "django.contrib.auth",
    "django.contrib.sites",
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # ... include the providers:
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    # Save pages to cache. Must be FIRST.
    "wagtailcache.cache.UpdateCacheMiddleware",
    # compress
    "django.middleware.gzip.GZipMiddleware",
    # Common functionality
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.CommonMiddleware",
    # Security
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    # Whitenoise
    "whitenoise.middleware.WhiteNoiseMiddleware",
    #  Error reporting. Uncomment this to recieve emails when a 404 is triggered.
    # 'django.middleware.common.BrokenLinkEmailsMiddleware',
    # CMS functionality
    "wagtail.core.middleware.SiteMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    # Fetch from cache. Must be LAST.
    "wagtailcache.cache.FetchFromCacheMiddleware",
]

ROOT_URLCONF = "webapps.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
            ],
        },
    },
]

WSGI_APPLICATION = "webapps.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

# To add or change language of the project, modify the list below.
LANGUAGE_CODE = "en-us"

LANGUAGES = [("en-us", _("English"))]

TIME_ZONE = "Asia/Jakarta"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/


STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# Javascript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/3.0/ref/contrib/staticfiles/#manifeststaticfilesstorage
# STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


# Login

LOGIN_URL = "wagtailadmin_login"
LOGIN_REDIRECT_URL = "wagtailadmin_home"

# Wagtail settings

WAGTAIL_SITE_NAME = "LiniMuda"
WAGTAIL_ENABLE_UPDATE_CHECK = False

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = "linimuda.co.id"

# Search
ROOT_DIR = os.path.abspath(os.path.dirname(__name__))

WAGTAILSEARCH_BACKENDS = {"default": {"BACKEND": "wagtail.search.backends.db",}}
# LIBRARY NYA ADA YANG ERROR, DIPAKAI KALAU PULL REQUEST UDAH BENAR
# WAGTAILSEARCH_BACKENDS = {
#     "default": {
#         "BACKEND": "wagtail_whoosh.backend",
#         "PATH": os.path.join(ROOT_DIR, "search_index"),
#         "LANGUAGE": "en",
#     }
# }


# Bootstrap

BOOTSTRAP4 = {
    # set to blank since coderedcms already loads jquery and bootstrap
    "jquery_url": "",
    "base_url": "",
    # remove green highlight on inputs
    "success_css_class": "",
}


# Tags
TAGGIT_CASE_INSENSITIVE = True

# Django Allauth
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

# Provider specific settings allauth
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '69742839210-pfu31324mq4dv23bd4tc6g4o6b2ftpv1.apps.googleusercontent.com',
            'secret': 'bg4qTumhl7SdUFU1dtt7R4ey',
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_USERNAME_BLACKLIST = ["admin", "god"]
ACCOUNT_USERNAME_MIN_LENGTH = 2