#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    if os.getenv("PYTHON_ENV"):
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE", "website_insanq_project.settings.prod"
        )
    else:
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE", "website_insanq_project.settings.dev"
        )

    from django.core.management import execute_from_command_line  # noqa

    execute_from_command_line(sys.argv)
