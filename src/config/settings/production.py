import os

from config.settings.base import *
from config.settings.base import BASE_DIR, env

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DJANGO_DB_NAME"),
        "USER": env("DJANGO_DB_USER"),
        "PASSWORD": env("DJANGO_DB_PASSWORD"),
        "HOST": env("DJANGO_DB_HOST"),
        "PORT": env("DJANGO_DB_PORT"),
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Definir la ruta en donde se guaradaran los ficheros MEDIA
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
