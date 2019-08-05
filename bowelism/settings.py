import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '9h7!s%##^!7!8tzbl!6dur!4w_3@98d0nk2%z^)y#6p#-a(n+o'

DEBUG = bool(os.environ.get('DEBUG', False))
ADMIN = bool(os.environ.get('ADMIN', False))
PRODUCTION = bool(os.environ.get('PRODUCTION', False))

if PRODUCTION:
    DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = ((['django.contrib.admin'] if ADMIN else []) + [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',

    'channels',
    'bowelism.api',
    'bowelism.log_streaming',
])

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bowelism.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'bowelism', 'templates')
        ],
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

WSGI_APPLICATION = 'bowelism.wsgi.application'
ASGI_APPLICATION = 'bowelism.routing.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}

TIME_ZONE = 'UTC'

STATIC_URL = '/static/'
STATIC_ROOT = '/static'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'bowelism', 'media')
]

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

STREAMED_LOG_FILE = os.environ.get('STREAMED_LOG_FILE', 'test_log.txt')
STREAMING_LOG_GROUP = 'log_streaming'

if PRODUCTION:
    EXTRA_INSTALLED_APPS = ()

    from bowelism.settings_production import *  # NOQA

    INSTALLED_APPS += EXTRA_INSTALLED_APPS
