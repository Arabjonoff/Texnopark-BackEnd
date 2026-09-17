"""
Andijon Yoshlar Texnoparki — backend sozlamalari.

Maxfiy va muhitga bog'liq qiymatlar `.env` faylidan o'qiladi (namuna: `.env.example`).
"""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')


def env_list(name, default=''):
    return [item.strip() for item in os.getenv(name, default).split(',') if item.strip()]


SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-dev-only-change-me')

DEBUG = os.getenv('DJANGO_DEBUG', 'True').lower() in ('1', 'true', 'yes')

ALLOWED_HOSTS = env_list('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1')

# Admin panel HTTPS domen orqali ochilganda CSRF tekshiruvi uchun, masalan: https://texnopark.uz
CSRF_TRUSTED_ORIGINS = env_list('DJANGO_CSRF_TRUSTED_ORIGINS')

# Saytning ochiq manzili. Rasm URL'lari shu domen bilan qaytadi — aks holda frontend serveri
# API'ga ichki manzil (http://backend:8000) orqali murojaat qilgani uchun rasmlar brauzerda ochilmaydi.
PUBLIC_BASE_URL = os.getenv('PUBLIC_BASE_URL', '').rstrip('/')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_filters',
    'drf_spectacular',
    # Local
    'apps.core',
    'apps.courses',
    'apps.events',
    'apps.content',
    'apps.projects',
    'apps.news',
    'apps.applications',
    'apps.dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # Docker'da ma'lumotlar volume ichida saqlanadi (SQLITE_PATH=/app/data/db.sqlite3)
        'NAME': os.getenv('SQLITE_PATH', BASE_DIR / 'db.sqlite3'),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


LANGUAGE_CODE = 'uz'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = f'{PUBLIC_BASE_URL}/media/' if PUBLIC_BASE_URL else 'media/'
MEDIA_ROOT = Path(os.getenv('MEDIA_ROOT', BASE_DIR / 'media'))

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


if not DEBUG:
    # Nginx HTTPS'ni qabul qilib, ichkariga HTTP orqali uzatadi
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'root': {'handlers': ['console'], 'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO')},
}


MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}


# CORS — Next.js frontend manzillari
CORS_ALLOWED_ORIGINS = env_list('CORS_ALLOWED_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000')


REST_FRAMEWORK = {
    # API frontend bilan bir xil camelCase formatda javob beradi va qabul qiladi
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
    ),
    'JSON_UNDERSCOREIZE': {'no_underscore_before_number': True},
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # Formalar (POST /api/applications/) uchun spamga qarshi cheklov
    'DEFAULT_THROTTLE_RATES': {
        'applications': os.getenv('APPLICATIONS_THROTTLE_RATE', '10/hour'),
        # Dashboard login: parolni tanlab topishga qarshi
        'login': os.getenv('LOGIN_THROTTLE_RATE', '5/minute'),
    },
}

# Dashboard sessiyasi (token) amal qilish muddati, soat
DASHBOARD_TOKEN_TTL_HOURS = int(os.getenv('DASHBOARD_TOKEN_TTL_HOURS', '72'))

SPECTACULAR_SETTINGS = {
    'TITLE': 'Andijon Yoshlar Texnoparki API',
    'DESCRIPTION': "Texnopark sayti uchun REST API: kurslar, tadbirlar, yangiliklar, sayt kontenti va murojaatlar.",
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'CAMELIZE_NAMES': True,
    # "status" nomi ikki modelda ishlatiladi — sxemada aniq nom beriladi
    'ENUM_NAME_OVERRIDES': {
        'EventStatusEnum': 'apps.events.models.Event.Status',
        'ApplicationStatusEnum': 'apps.applications.models.Application.Status',
        'ApplicationTypeEnum': 'apps.applications.models.Application.Type',
    },
    'POSTPROCESSING_HOOKS': [
        'drf_spectacular.contrib.djangorestframework_camel_case.camelize_serializer_fields',
        'drf_spectacular.hooks.postprocess_schema_enums',
    ],
}
