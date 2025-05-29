from pathlib import Path
import os
from datetime import timedelta
from decouple import config, Csv
from dotenv import load_dotenv
import dj_database_url
import ssl
import certifi
from urllib.parse import urlparse

# Load .env variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# Disable APPEND_SLASH to prevent issues with API endpoints without trailing slashes
APPEND_SLASH = False

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',    # Third-party apps
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',  # JWT token blacklist support
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'django_rest_passwordreset',
    'drf_spectacular',

    # Local apps
    'users.apps.UsersConfig',
    'children',
    'taskmaster',
    'familywallet',
    'insighttracker',
    'settings_waya',
]

AUTH_USER_MODEL = 'users.User'

# === Corrected allauth + dj-rest-auth settings ===
# Remove deprecated settings: ACCOUNT_AUTHENTICATION_METHOD, ACCOUNT_EMAIL_REQUIRED, ACCOUNT_USERNAME_REQUIRED

ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']  # Asterisks indicate required fields
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # Options: 'mandatory', 'optional', 'none'
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'users.serializers.UserRegistrationSerializer',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'users.middleware.CustomErrorHandlingMiddleware',
]

ROOT_URLCONF = 'waya_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'waya_backend', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Required by allauth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'waya_backend.wsgi.application'

# Database
# DATABASES = {
#     'default': dj_database_url.config(
#         default=config('DATABASE_URL'),
#         conn_max_age=600,
#         ssl_require=False
#     )
# }


# Replace the DATABASES section of your settings.py with this
tmpPostgres = urlparse(os.getenv("DATABASE_URL"))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': tmpPostgres.path.replace('/', ''),
        'USER': tmpPostgres.username,
        'PASSWORD': tmpPostgres.password,
        'HOST': tmpPostgres.hostname,
        'PORT': 5432,
    }
}

# DATABASES = {
#         'default': dj_database_url.config(
#             default=config('DATABASE_URL'),
#             conn_max_age=600,
#             conn_health_checks=True,
#             ssl_require=True
#         )
#     }

# Celery settings
CELERY_BROKER_URL = 'redis://localhost:6379/0' 
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static & Media Files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Required for collectstatic
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 2525
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = config('SENDGRID_API_KEY')
SENDGRID_SENDER_EMAIL = config('SENDGRID_SENDER_EMAIL', default='ogunsemorepresh@gmail.com')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default=SENDGRID_SENDER_EMAIL)

# SSL Certificates for requests
ssl_context = ssl.create_default_context(cafile=certifi.where())

# Django REST Framework and JWT
REST_USE_JWT = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# drf-spectacular settings for OpenAPI/Swagger documentation
SPECTACULAR_SETTINGS = {
    'TITLE': 'Waya Backend API',
    'DESCRIPTION': 'API documentation for Waya Backend - A comprehensive family management and task tracking system',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': r'/api/',
    'SCHEMA_PATH_PREFIX_TRIM': True,
    'TAGS': [
        {'name': 'Authentication', 'description': 'User authentication and registration endpoints'},
        {'name': 'Users', 'description': 'User management operations'},
        {'name': 'Children', 'description': 'Child profile management'},
        {'name': 'Tasks', 'description': 'Task management and tracking'},
        {'name': 'Family Wallet', 'description': 'Family financial management'},
        {'name': 'Insights', 'description': 'Analytics and insights tracking'},
        {'name': 'Settings', 'description': 'Application settings management'},
    ],
    'AUTHENTICATION_WHITELIST': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': False,
        'defaultModelsExpandDepth': 1,
        'defaultModelExpandDepth': 1,
        'defaultModelRendering': 'example',
        'displayRequestDuration': True,
        'docExpansion': 'none',
        'filter': True,
        'showExtensions': True,
        'showCommonExtensions': True,
    },
    'REDOC_UI_SETTINGS': {
        'hideDownloadButton': False,
        'hideHostname': False,
        'hideLoading': False,
        'hideSchemaPattern': True,
        'expandResponses': '200,201',
        'pathInMiddlePanel': True,
        'nativeScrollbars': False,
        'theme': {
            'colors': {
                'primary': {
                    'main': '#3f51b5'
                }
            },
            'typography': {
                'fontSize': '14px',
                'lineHeight': '1.5em',
                'code': {
                    'fontSize': '13px'
                }
            }
        }
    }
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:8000",
]

FRONTEND_URL = "http://localhost:8000"

# Social Account Providers
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': config('GOOGLE_CLIENT_ID'),
            'secret': config('GOOGLE_CLIENT_SECRET'),
            'key': ''
        }
    }
}

# Security Headers (for production)
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True

# URL Configuration
APPEND_SLASH = False  # Disable automatic slash appending to match URL patterns

# Production settings for Render
import os
import sys

# Add Render domain to ALLOWED_HOSTS if RENDER environment variable exists
if 'RENDER' in os.environ:
    ALLOWED_HOSTS.append(os.environ.get('RENDER_EXTERNAL_HOSTNAME'))

# Static files configuration for production
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Additional static files directories
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
] if os.path.exists(os.path.join(BASE_DIR, 'static')) else []

# WhiteNoise configuration for serving static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Database configuration with fallback
if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.parse(os.environ.get('DATABASE_URL'))
    # SSL configuration for production database
    DATABASES['default']['OPTIONS'] = {
        'sslmode': 'require',
    }
