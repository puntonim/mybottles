"""
Development settings.
"""

from .settings_base import *


DEBUG = True
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
