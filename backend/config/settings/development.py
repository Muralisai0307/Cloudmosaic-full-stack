from .base import *

DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

# Use console backend for emails during development if not using actual SMTP
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
