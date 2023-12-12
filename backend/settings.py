import os
import sys

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "N!.1>u7:*R8uuqI}LBYVG~C6<xN_cn[@<e:7Ev0i\0fLy|rX'l`!yt#r(WU/c$7b",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"
TESTING = "test" in sys.argv

CORS_ALLOWED_ORIGINS = [os.getenv("CORS_ORIGIN_WHITELIST", "http://localhost:3000")]

ALLOWED_HOSTS = [os.getenv("ALLOWED_HOSTS", "*")]

CSRF_TRUSTED_ORIGINS = [
    os.getenv("CORS_ORIGIN_WHITELIST", "http://localhost:3000"),
    os.getenv("BACKEND_ORIGIN", "http://localhost:8000"),
]

# Application definition
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django_extensions",
    "rest_framework",
    "corsheaders",
    "django_q",
    "api.apps.Config",
    "workers.apps.Config",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "urls"

WSGI_APPLICATION = "wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.getenv("DB_NAME", "postgres"),
        "USER": os.getenv("DB_USER", "postgres"),
        "PASSWORD": os.getenv("DB_PASSWORD", "postgres"),
        "HOST": os.getenv("DB_HOST", "db"),
        "PORT": os.getenv("DB_PORT", "5432"),
    },
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Canada/Pacific"
USE_TZ = True

# Django Rest Framework Settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

Q_CLUSTER = {
    "name": "VDCD",
    "workers": 4,
    "timeout": 90,
    "retry": 120,
    "queue_limit": 50,
    "bulk": 10,
    "orm": "default",
    "save_limit": -1,
    "max_attempts": 100,
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    },
}

FRONTEND_APP_NAME = "frontend"

MAX_DECODE_ATTEMPTS = os.getenv("MAX_DECODE_ATTEMPTS", 5)

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM")

MINIO_ACCESS_KEY = os.getenv("MINIO_ROOT_USER")
MINIO_SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD")
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_USE_SSL = os.getenv("MINIO_USE_SSL", False)

VPIC_ENDPOINT = os.getenv(
    "VPIC_ENDPOINT",
    "https://vpic.nhtsa.dot.gov/api/vehicles",
)
VPIC_VIN_KEY = os.getenv("VPIC_VIN_KEY", "VIN")
VPIC_ERROR_CODE_NAME = os.getenv("VPIC_ERROR_CODE_NAME", "ErrorCode")
VPIC_SUCCESS_ERROR_CODE = os.getenv("VPIC_SUCCESS_ERROR_CODE", "0")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "healthcheck": {
            "()": "api.logging_filters.HealthcheckFilter",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "filters": ["healthcheck"],
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
        },
    },
}
