"""
TravisCI settings.
"""
# flake8: noqa F405 F403

from .settings_base import *

DEBUG = True
ALLOWED_HOSTS = ['*']
SECRET_KEY = 'mysecretkey'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DJANGO REST FRAMEWORK.
REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = ['rest_framework.permissions.AllowAny']

# Remove haystack from INSTALLED_APP.
INSTALLED_APPS.remove('haystack')
