#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # Render sets RENDER=true on every service automatically — fall back to
    # production settings there even if DJANGO_SETTINGS_MODULE isn't set
    # explicitly in the dashboard, since that's been a recurring deploy
    # failure (debug_toolbar, a dev-only dependency, isn't installed in
    # production and development.py requires it).
    default_settings = (
        'config.settings.production'
        if os.environ.get('RENDER')
        else 'config.settings.development'
    )
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', default_settings)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
