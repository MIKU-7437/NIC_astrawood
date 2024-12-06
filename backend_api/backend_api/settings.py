import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-kq8()8@%=e$cae!p$+abx+r6cw(8#wqh=xqk^rdtj#sb&%khlf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', False)

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')  # замените на имя вашего бакета
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')  # замените на ваш регион
AWS_QUERYSTRING_AUTH = False  # отключить подписи для публичного доступа

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',

    'store',
    'users',
    'custom_auth',

    'storages',


    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'backend_api.urls'

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

WSGI_APPLICATION = 'backend_api.wsgi.application'

# Database configuration
if os.environ.get('POSTGRES_DB') and os.environ.get('POSTGRES_USER'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB'),
            'USER': os.environ.get('POSTGRES_USER'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
            'PORT': os.environ.get('POSTGRES_PORT'),
            'HOST': os.environ.get('POSTGRES_HOST'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static and media files
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/static/'

# Media files
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/'
# AWS S3 Configuration
AWS_ACCESS_KEY_ID = "h6E9GzDHv6fqujJHrDUqna"
AWS_SECRET_ACCESS_KEY = "8sgjRzj4cEF2x9yoiE2zsrhD9XfNg3yuwGvHKf2qMrCS"
AWS_STORAGE_BUCKET_NAME = "product_photos"
AWS_S3_ENDPOINT_URL = "https://testbucketabay.hb.kz-ast.bizmrg.com/"
AWS_QUERYSTRING_AUTH = False  # Отключить подписи для ссылок (опционально)

# Использовать S3 как основное хранилище медиа
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# URL для доступа к загруженным файлам
MEDIA_URL = f"{AWS_S3_ENDPOINT_URL}/"
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR.parent, "staticfiles/")
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static/')]
# MEDIA_ROOT = os.path.join(BASE_DIR.parent, 'media')
# MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = [
    'https://astrawood-production.up.railway.app',
    'http://astrawood-production.up.railway.app',
]
CORS_ALLOW_ALL_ORIGINS = True

# Django Rest Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

# Custom user model
AUTH_USER_MODEL = 'users.User'

# Email send settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '{asctime} {levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'detailed',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'detailed',
        },
    },
    'loggers': {
        'email': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Настройки Celery
CELERY_BROKER_URL = os.getenv("REDIS_URL", 'redis://localhost:6379/0')  # Адрес Redis
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"

# Настройки для хранения результатов (опционально)
CELERY_RESULT_BACKEND = os.getenv("REDIS_URL", 'redis://localhost:6379/0')
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
CELERY_ENABLE_UTC = True



# AWS S3 Configuration
AWS_ACCESS_KEY_ID = "h6E9GzDHv6fqujJHrDUqna"
AWS_SECRET_ACCESS_KEY = "8sgjRzj4cEF2x9yoiE2zsrhD9XfNg3yuwGvHKf2qMrCS"
AWS_STORAGE_BUCKET_NAME = "testbucketabay"
AWS_S3_ENDPOINT_URL = "https://testbucketabay.hb.kz-ast.bizmrg.com/"
AWS_QUERYSTRING_AUTH = False  # Отключить подписи для публичного доступа

# Использовать S3 как основное хранилище медиа
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# URL для доступа к загруженным файлам
MEDIA_URL = f"{AWS_S3_ENDPOINT_URL}"
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
