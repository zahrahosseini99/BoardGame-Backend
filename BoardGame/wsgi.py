"""
WSGI config for BoardGame project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
import sys


path = '/home/zahrahosseini99/BoardGame-Backend'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'BoardGame.settings'

from django.core.wsgi import get_wsgi_application


application = get_wsgi_application()
