"""
Django settings for cold_fusion_fishing project.

Generated by 'django-admin startproject' using Django 4.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
env.read_env(env_file=BASE_DIR / '.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY', 'secret_key')
# SECRET_KEY = 'django-insecure-m%y4*9@i39$=yj&i_&)f=pgz4)u0nmht178e@)eg&4-$dva5z%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])
WAITRESS_HOST = env.str('WAITRESS_HOST', default='0.0.0.0')
WAITRESS_PORT = env.int('WAITRESS_PORT', default=8000)

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env.bool("SECURE_REDIRECT", default=False)
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"

ENABLE_BROWSER_RELOAD = env.bool("ENABLE_BROWSER_RELOAD", default=False)

# Application definition

INSTALLED_APPS = [
    'sslserver',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCAL_APPS = [
    'api_modules.apps.ApiModulesConfig',
    'users.apps.UsersConfig',
    'projects.apps.ProjectsConfig',
    'home.apps.HomeConfig',
    'fish_tanks.apps.FishTanksConfig',
    'modules.apps.ModulesConfig',
    'dashboard.apps.DashboardConfig',
]

THIRD_PARTY_APPS = [
    'tailwind',
    'theme.apps.ThemeConfig',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_htmx',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    'crispy_forms',
    'crispy_tailwind',
    'widget_tweaks',
    'mathfilters',
    'django_filters',
    'corsheaders',
]

if ENABLE_BROWSER_RELOAD:
    THIRD_PARTY_APPS += [
        'django_browser_reload',
    ]

INSTALLED_APPS += LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

THIRD_PARTY_MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]

if ENABLE_BROWSER_RELOAD:
    THIRD_PARTY_MIDDLEWARE += [
        'django_browser_reload.middleware.BrowserReloadMiddleware',
    ]

MIDDLEWARE += THIRD_PARTY_MIDDLEWARE

ROOT_URLCONF = 'cold_fusion_fishing.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'theme.context_processors.theme',
            ],
        },
    },
]

WSGI_APPLICATION = 'cold_fusion_fishing.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': env.str('MYSQL_DATABASE_NAME', ''),
    #     'USER': env.str('MYSQL_USER', ''),
    #     'PASSWORD': env.str('MYSQL_PASSWORD', ''),
    #     'HOST': env.str('MYSQL_HOST', 'localhost'),
    #     'PORT': env.str('MYSQL_PORT', 3306),
    # }
}

DATABASE_URL = env.str('DATABASE_URL', default=None)
if DATABASE_URL:
    DATABASES = {
        'default': env.db(),
    }
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

AUTH_USER_MODEL = 'users.User'

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'theme/static'),
    # BASE_DIR / 'theme' / 'static',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# email settings
DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL', 'admin@admin.com')
EMAIL_SUBJECT_PREFIX = env.str('EMAIL_SUBJECT_PREFIX', '')

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# locale settings
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale/'),
]

LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', 'English'),
    ('bn', 'Bangla'),
]

USE_I18N = True
USE_L10N = True

SHORT_DATE_FORMAT = 'd M Y'
DATE_INPUT_FORMATS = ['%d-%m-%Y', '%Y-%m-%d']

# tailwind settings
TAILWIND_APP_NAME = 'theme'
TAILWIND_DEV_MODE = DEBUG
TAILWIND_CSS_PATH = 'tailwind/css/styles.css'

NPM_BIN_PATH = env.str('NPM_BIN_PATH', r'C:\Program Files\nodejs\npm.cmd')

if DEBUG:
    INTERNAL_IPS = [
        "127.0.0.1",
    ]

# allauth settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

# django rest framework
# rest framework settings
DEFAULT_AUTHENTICATION_CLASSES = [
    'rest_framework.authentication.BasicAuthentication',
    'rest_framework.authentication.TokenAuthentication',
]

if DEBUG:
    DEFAULT_AUTHENTICATION_CLASSES += [
        'rest_framework.authentication.SessionAuthentication',
    ]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'api_modules.paginations.StandardNumberPagination',
    'PAGE_SIZE': 25,
    'DEFAULT_AUTHENTICATION_CLASSES': DEFAULT_AUTHENTICATION_CLASSES,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.AllowAny',
    ],
}

CORS_ALLOW_ALL_ORIGINS = env.bool('CORS_ALLOW_ALL_ORIGINS', default=True)

# Debug toolbar settings
if DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]
    INTERNAL_IPS = ['127.0.0.1', ]
    import mimetypes

    mimetypes.add_type("application/javascript", ".js", True)
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }

# crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = 'tailwind'
CRISPY_TEMPLATE_PACK = 'tailwind'

CRISPY_CLASS_CONVERTERS = {
    # 'textinput': 'input',
}

DATE_INPUT_FORMATS = ('%d-%m-%Y', '%Y-%m-%d')

# SECURE_CONTENT_TYPE_NOSNIFF = False
# SECURE_BROWSER_XSS_FILTER = False
# # SECURE_SSL_REDIRECT = False
# SESSION_COOKIE_SECURE = False
# CSRF_COOKIE_SECURE = False
# X_FRAME_OPTIONS = 'DENY'

REDIS_URL = env.str('REDIS_URL', 'redis://localhost:6379')
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=['localhost', ])
