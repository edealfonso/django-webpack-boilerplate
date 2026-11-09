from .base import *

import mimetypes

mimetypes.add_type("text/css", ".css", True)


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False

# e.g. ALLOWED_HOSTS=example.com,www.example.com
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# e.g. CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])
