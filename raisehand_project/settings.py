"""
Django settings for RaiseHand Lite project.

This project uses Django Channels for WebSocket support,
enabling real-time communication between students and teachers.

Key Features:
- ASGI application support via Daphne
- Redis channel layer for message broadcasting
- WebSocket routing for classroom interactions
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# In production, use environment variable: os.environ.get('SECRET_KEY')
SECRET_KEY = 'django-insecure-raisehand-lite-dev-key-change-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']


# Application definition
# Note: 'daphne' must be listed first for ASGI support
INSTALLED_APPS = [
    'daphne',  # ASGI server - must be first for proper ASGI handling
    'channels',  # Django Channels for WebSocket support
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'classroom',  # Our main application for raise hand functionality
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

ROOT_URLCONF = 'raisehand_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application (for traditional HTTP)
WSGI_APPLICATION = 'raisehand_project.wsgi.application'

# ASGI application (for WebSocket + HTTP)
# This is the entry point for Daphne server
ASGI_APPLICATION = 'raisehand_project.asgi.application'


# =============================================================================
# DJANGO CHANNELS CONFIGURATION
# =============================================================================
# Channel layers allow different instances of an application 
# to communicate with each other in real-time.

# For development WITHOUT Redis, use InMemoryChannelLayer
# Note: This doesn't work across multiple processes, but is fine for testing
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# For production WITH Redis, uncomment below and comment out above:
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             # Redis connection - default local Redis
#             # In production, use: redis://<username>:<password>@<host>:<port>
#             'hosts': [('127.0.0.1', 6379)],
#             # Group expiry time (in seconds)
#             'group_expiry': 86400,  # 24 hours
#         },
#     },
# }


# Database
# Using SQLite for simplicity - in production use PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'  # Indian Standard Time
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
