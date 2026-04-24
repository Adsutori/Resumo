"""
Django settings for Resumo project.
"""

from pathlib import Path
from decouple import config
from urllib.parse import urlparse, parse_qsl

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================================================
# SECURITY
# ==============================================================

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost').split(',')


# ==============================================================
# APPLICATIONS
# ==============================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lucide',
    'django_apscheduler',
    # Local
    'Users',
    'Dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Resumo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
            'builtins': [
                'lucide.templatetags.lucide',  # usuń jeśli nie używasz django-lucide
            ],
        },
    },
]

WSGI_APPLICATION = 'Resumo.wsgi.application'


# ==============================================================
# DATABASE — Neon PostgreSQL
# Reads DATABASE_URL from .env and parses it
# ==============================================================

_db_url = urlparse(config('DATABASE_URL'))

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql',
        'NAME':     _db_url.path.lstrip('/'),   # usuwa wiodący "/"
        'USER':     _db_url.username,
        'PASSWORD': _db_url.password,
        'HOST':     _db_url.hostname,
        'PORT':     _db_url.port or 5432,
        'OPTIONS': {
            **dict(parse_qsl(_db_url.query)),   # wyciąga sslmode=require z URL
            'sslmode': 'require',               # fallback — Neon zawsze wymaga SSL
        },
    }
}


# ==============================================================
# PASSWORD VALIDATION
# ==============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



# ==============================================================
# INTERNATIONALISATION
# ==============================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'UTC'
USE_I18N      = True
USE_TZ        = True


# ==============================================================
# STATIC FILES
# ==============================================================

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==============================================================
# EMAIL — Gmail SMTP
# ==============================================================

EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_PORT          = 587
EMAIL_USE_TLS       = True
EMAIL_HOST_USER     = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL  = f'Resumo <{config("EMAIL_HOST_USER")}>'


# ==============================================================
# AUTH REDIRECTS
# ==============================================================

LOGIN_URL           = '/users/login/'
LOGIN_REDIRECT_URL  = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# Własny model użytkownika
AUTH_USER_MODEL = 'Users.User'

# Backend logowania przez email
AUTHENTICATION_BACKENDS = [
    'Users.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Przekierowania
LOGIN_URL           = '/users/login/'
LOGIN_REDIRECT_URL  = '/users/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# Media (avatary)
MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE    = 'Lax'

SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 60 * 60 * 24 * 14

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
APSCHEDULER_RUN_NOW_TIMEOUT = 25