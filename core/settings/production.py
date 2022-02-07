import os

import dj_database_url

from .base import *  # noqa


DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASES['default'] = dj_database_url.config(default=DATABASE_URL)
