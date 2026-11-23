INSTALLED_APPS = [
    # Django 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_browser_reload',
    'debug_toolbar',
    # Django rest framework
    'rest_framework_simplejwt',
    'rest_framework',
    # Estes são nossos apps
    'recipes',
    'authors',
    'tags'
]

from datetime import timedelta
import os

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(minutes=10),
    "BLACKLIST_AFTER_ROTATION": False,
    "SIGNING_KEY": os.environ.get('SECRET_KEY_JWT', 'INSECURE'),
    "AUTH_HEADER_TYPES": ("Bearer",),
}