"""
TravisCI settings.
"""

from .settings_base import *  # noqa F403

DEBUG = True
ALLOWED_HOSTS = ['*']
SECRET_KEY = 'mysecretkey'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),  # noqa F405
    }
}

# DJANGO REST FRAMEWORK.
REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = ['rest_framework.permissions.AllowAny']  # noqa F405
