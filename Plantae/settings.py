from pathlib import Path
import os
from dotenv import load_dotenv

#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) --> Antiga
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')

TARGET_ENV = os.getenv('TARGET_ENV')
NOT_PROD = not TARGET_ENV.lower().startswith('prod')

if NOT_PROD:
    DEBUG = True
    SECRET_KEY = 'i8e1s3!_(fjsiv%1pn3sb3o=s)!p*nzwh1$gp5-l&%nb!d=y_s'
    ALLOWED_HOSTS = []
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    SECRET_KEY = os.getenv('i8e1s3!_(fjsiv%1pn3sb3o=s)!p*nzwh1$gp5-l&%nb!d=y_s')
    DEBUG = os.getenv('DEBUG', '0').lower() in ['true', 't', '1']
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(' ')
    CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS').split(' ')

    SECURE_SSL_REDIRECT = \
        os.getenv('SECURE_SSL_REDIRECT', '0').lower() in ['true', 't', '1']

    if SECURE_SSL_REDIRECT:
        SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DBNAME'),
            'HOST': os.environ.get('DBHOST'),
            'USER': os.environ.get('DBUSER'),
            'PASSWORD': os.environ.get('DBPASS'),
            'OPTIONS': {'sslmode': 'require'},
        }
    }
    
# Application definition

DEFAULT_AUTO_FIELD='django.db.models.AutoField' 

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "site_cc.apps.SiteCcConfig",
    "accounts.apps.AccountsConfig",
    "whitenoise.runserver_nostatic",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",                            
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "Plantae.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "Plantae.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation." "MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation." "CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation." "NumericPasswordValidator"},
]

AUTH_USER_MODEL = "accounts.User"

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_L10N = True

USE_TZ = False

STATIC_URL = os.environ.get('DJANGO_STATIC_URL', "/static/")
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = ('whitenoise.storage.CompressedManifestStaticFilesStorage')

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'