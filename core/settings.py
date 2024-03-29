from pathlib import Path
import os

from google.cloud import secretmanager
from google.cloud.secretmanager_v1.types.service import AccessSecretVersionRequest
from google.api_core import retry

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "uix1bor_miw*cxrs#hn1bz(z=qmdfja08dcrc$bu6y3+n_y^u0"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "lab.apps.LabConfig",
    "users.apps.UsersConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Django all auth
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # Django anymail
    "anymail",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "assets"),)
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Django auth
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Users

AUTH_USER_MODEL = "users.LabUser"


# Django all auth

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_ID = 1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
ACCOUNT_FORMS = {
    "login": "users.forms.LabLoginForm",
    "signup": "users.forms.LabSignUpForm",
}
ACCOUNT_USER_DISPLAY = "users.utils.user_display"


# Google Cloud
def get_secret(client, project_id, key):
    """
    Get secrets from Secret Manager
    """
    resource_id = f"projects/{project_id}/secrets/{key}/versions/latest"
    res = client.access_secret_version(
        request={"name": resource_id}, retry=retry.Retry()
    )
    return res.payload.data.decode("UTF-8")


if os.environ.get("DEBUG"):
    DEBUG = False
    GCP_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
    client = secretmanager.SecretManagerServiceClient()
    SECRET_KEY = (get_secret(client, GCP_PROJECT, "SECRET_KEY"),)

    DATABASES = {
        "default": {
            "ENGINE": get_secret(client, GCP_PROJECT, "DATABASE_ENGINE"),
            "HOST": get_secret(client, GCP_PROJECT, "DATABASE_HOST"),
            "NAME": get_secret(client, GCP_PROJECT, "DATABASE_NAME"),
            "USER": get_secret(client, GCP_PROJECT, "DATABASE_USER"),
            "PASSWORD": get_secret(client, GCP_PROJECT, "DATABASE_PASSWORD"),
        }
    }

    # Djano anymail
    ANYMAIL = {
        "MAILGUN_API_KEY": get_secret(client, GCP_PROJECT, "MAILGUN_API_KEY"),
        "MAILGUN_SENDER_DOMAIN": get_secret(
            client, GCP_PROJECT, "MAILGUN_SENDER_DOMAIN"
        ),
    }
    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
    DEFAULT_FROM_EMAIL = "admin@lab.sarmad.ai"
    SERVER_EMAIL = "admin@lab.sarmad.ai"
