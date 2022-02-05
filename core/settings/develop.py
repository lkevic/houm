import os

import dj_database_url

from .base import *  # noqa


DEBUG = True

SECRET_KEY = os.environ.get('SECRET_KEY', default='django-insecure-rgw9f*!&76od#(an#6y($sh7ysz^idd&f0c4sc**3@g%$vfyoc')

DATABASE_URL = os.environ.get('DATABASE_URL', default=f'sqlite:////{BASE_DIR}/db.sqlite3')
DATABASES['default'] = dj_database_url.config(default=DATABASE_URL)

SHOW_DOCS = True
