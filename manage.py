#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "website_insanq_project.settings.dev"
    )

    from django.core.management import execute_from_command_line  # noqa

    execute_from_command_line(sys.argv)
