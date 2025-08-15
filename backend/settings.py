import os
from pathlib import Path
from decouple import config
from datetime import timedelta

SECRET_KEY = config("SECRET_KEY")


BASE_DIR = Path(__file__).resolve().parent.parent


DEBUG = True


ALLOWED_HOSTS = ['localhost', '127.0.0.1']


CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"
CELERY_BEAT_SCHEDULE = {
    "weekly-report-task": {
        "task": "transactions.tasks.generate_weekly_reports",
        "schedule": 604800.0,  # 1 hafta = 7 gün
    },
}


# Uygulamalar
INSTALLED_APPS = [
    'django.contrib.admin',
    'transactions',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  # collectstatic için gerekli


    'accounts',
    'reports',

    # drf-spectacular için
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'drf_yasg',
]
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Banka Ekstre API',
    'DESCRIPTION': 'Bu API banka ekstrelerini yönetmek için geliştirilmiştir.',
    'VERSION': '1.0.0',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'banka_user',
        'PASSWORD': 'banka_pass',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Parola validasyonları
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Dil ve zaman ayarları
LANGUAGE_CODE = 'tr-tr'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_TZ = True

# Statik dosya ayarları
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Varsayılan primary key tipi
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SWAGGER_USE_COMPAT_RENDERERS = False

