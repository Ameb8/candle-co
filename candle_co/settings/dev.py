from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.1.78', '192.168.1.77']

SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SECURE = False

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://192.168.1.78:5173",
    "http://192.168.1.77:5173",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}