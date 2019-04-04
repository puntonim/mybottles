"""
Development settings.
"""
from datetime import datetime

from .settings_base import *

DEBUG = True

HEADER = '\033[95m'
ENDC = '\033[0m'
BOLD = '\033[1m'
print('\n {}{}** SETTINGS PAOLO {}'.format(HEADER, BOLD, datetime.now().isoformat()))
print(' ** DEBUG={}{}\n'.format(DEBUG, ENDC))

SECRET_KEY = 'secretkey'
AUTH_PASSWORD_VALIDATORS = []
ALLOWED_HOSTS = ['*']

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'dbname',
    #     'USER': 'dbuser',
    #     'PASSWORD': 'dbpass',
    #     'HOST': '127.0.0.1',
    #     'PORT': '5432',
    # },

    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DJANGO REST FRAMEWORK.
REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = ['rest_framework.permissions.AllowAny',]

INSTALLED_APPS += [
    'django_extensions',
]
