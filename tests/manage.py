#!/usr/bin/env python
import os
import sys

# This file is not normally used. The tests.py file has a little bit of magic
# at the bottom which starts django. The purpose of this file is merely to
# make it easier to start the testing app manually (e.g. with runserver) in
# order to debug the testing suite itself.

# Instead of having the directory of __file__ in the path, we want its parent
# directory, so that "tests.settings" and "tests.urls" will point to the
# correct location.
sys.path[0] = os.path.dirname(sys.path[0])

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
