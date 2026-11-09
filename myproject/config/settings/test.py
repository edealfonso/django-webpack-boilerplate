"""
Settings for running the test suite:

    python manage.py test --settings=config.settings.test

No `.env`, Postgres or webpack build needed.
"""
import os

os.environ.setdefault('SECRET_KEY', 'insecure-test-key')
os.environ.setdefault('DATABASE_URL', 'sqlite://:memory:')

from .base import *  # noqa: E402

DEBUG = False

ALLOWED_HOSTS = ['testserver']

# Always use in-memory SQLite, even if DATABASE_URL is set (e.g. inside compose)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']

# Render `render_bundle` tags without webpack-stats.json
WEBPACK_LOADER = {
    'DEFAULT': {
        'LOADER_CLASS': 'webpack_loader.loaders.FakeWebpackLoader',
    }
}
