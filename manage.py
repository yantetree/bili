#!/usr/bin/env python2
import os
import sys

if __name__ == "__main__":

    # Patch the gevent
    from gevent import monkey
    monkey.patch_all()

    cwd = os.path.dirname(__file__)
    root = cwd
    app_path = os.path.join(root, 'bili', 'apps')

    if app_path not in sys.path:
        sys.path.append(app_path)

    if root not in sys.path:
        sys.path.append(root)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bili.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
