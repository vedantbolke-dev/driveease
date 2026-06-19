"""
WSGI config for DriveEase project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'driveease.settings')
application = get_wsgi_application()
