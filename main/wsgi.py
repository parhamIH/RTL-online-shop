"""
WSGI config for main project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys

# مسیر پروژه Django
path = '/path/to/your/django/project'  # مسیر واقعی پروژه‌ات را بگذار
if path not in sys.path:
    sys.path.append(path)

# تنظیم متغیر محیطی
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

# import Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
