from .base import *
import dj_database_url

DEBUG = False


ALLOWED_HOSTS = ['candle-co.onrender.com']

# Security settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

CSRF_TRUSTED_ORIGINS = [
    "http://10.0.0.202:5173",
    "http://10.0.0.202:5174",
]

# Production database (already hosted)
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DB_URL'),
        conn_max_age=600,  # persistent connections
        ssl_require=True
    )
}