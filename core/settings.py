# business_app/business_app/core/settings.py
from pathlib import Path
import os
import environ

# Initialize django-environ
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Set the project's base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file during local development
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# --- SECURITY ---
# Raises Django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY')

# DEBUG is False by default, will be True only if DEBUG=True is in environment
DEBUG = env('DEBUG')

# --- HOSTS ---
# Get the Render external hostname from the RENDER_EXTERNAL_HOSTNAME env var
# If you are not using Render, you may need to adjust this
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS = [RENDER_EXTERNAL_HOSTNAME]
else:
    ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


SITE_ID = 1

# --- APPS ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic", # Add WhiteNoise
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "accounts",
    "jobs",
    "widget_tweaks",
]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware", # Add WhiteNoise middleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --- URL / WSGI ---
ROOT_URLCONF = "core.urls"
WSGI_APPLICATION = "core.wsgi.application"

# --- DATABASE ---
# Reads the DATABASE_URL environment variable
DATABASES = {
    'default': env.db(),
}


# --- PASSWORDS ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- AUTH ---
AUTH_USER_MODEL = "accounts.User"
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = '/accounts/dashboard-home/'
LOGOUT_REDIRECT_URL = "/accounts/login/"

CSRF_FAILURE_VIEW = 'accounts.views.csrf_failure'

# --- I18N ---
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# --- STATIC / MEDIA ---
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Enable WhiteNoise to serve static files in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --- TEMPLATES ---
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# --- EMAIL ---
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# --- DEFAULT PK ---
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
