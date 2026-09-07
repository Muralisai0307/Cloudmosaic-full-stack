from .base import *
import os

DEBUG = False

# Strict SECRET_KEY validation for production - NO FALLBACKS
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY or SECRET_KEY.startswith('django-insecure-'):
    from django.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured("SECRET_KEY environment variable is required and must be secure in production - NO FALLBACKS")

# Ensure this is set via environment variables in production - NO FALLBACKS
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
if '' in ALLOWED_HOSTS:
    ALLOWED_HOSTS.remove('')

CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
if '' in CORS_ALLOWED_ORIGINS:
    CORS_ALLOWED_ORIGINS.remove('')

CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')
if '' in CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS.remove('')

# Security settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'same-origin'
X_FRAME_OPTIONS = 'DENY'

# HSTS - Conservative configuration
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Disable AdminRenderer and Browsable API in production for security
REST_FRAMEWORK = {
    **REST_FRAMEWORK,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

# In production, use standard SMTP or another backend
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
