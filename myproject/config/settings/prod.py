from .base import *


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False

# e.g. ALLOWED_HOSTS=example.com,www.example.com
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# e.g. CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])


# HTTPS
# TLS is terminated in front of Django (nginx / load balancer), which must set
# X-Forwarded-Proto. Set SECURE_HTTPS=False only to try the prod stack over
# plain HTTP (e.g. locally).
# https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

SECURE_HTTPS = env.bool('SECURE_HTTPS', default=True)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = SECURE_HTTPS
SESSION_COOKIE_SECURE = SECURE_HTTPS
CSRF_COOKIE_SECURE = SECURE_HTTPS

# HSTS: start low (e.g. 3600) and raise to 31536000 once HTTPS works everywhere.
# Browsers remember it, so a mistake here is hard to undo.
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=False)
SECURE_HSTS_PRELOAD = env.bool('SECURE_HSTS_PRELOAD', default=False)
