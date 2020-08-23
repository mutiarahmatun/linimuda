#!/usr/bin/env python
import os
import sys
import environ
from django.core.exceptions import ImproperlyConfigured

if __name__ == "__main__":
    env = environ.Env()
    environ.Env.read_env()
    try:
        if env("PYTHON_ENV") == "production":
            os.environ.setdefault(
                "DJANGO_SETTINGS_MODULE", "website_insanq_project.settings.prod"
            )
        else:
            raise ImproperlyConfigured
    except ImproperlyConfigured:
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE", "website_insanq_project.settings.dev"
        )

    from django.core.management import execute_from_command_line  # noqa

    execute_from_command_line(sys.argv)
