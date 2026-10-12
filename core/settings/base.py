"""
Base settings shared between all environments.
Do NOT use this file directly — use local.py or production.py.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# ─── Paths ───────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / "Storage" / ".env")

# ─── Security ─────────────────────────────────────────────────────────────────
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-change-me-in-production")

# ─── Applications ─────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    "daphne",
    "channels",
    "django_extensions",
    "django_browser_reload",
    "jazzmin",
    "django_filters",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "Admin.apps.AdminConfig",
    "Engineer.apps.EngineerConfig",
    "Client.apps.ClientConfig",
    "Visits.apps.VisitsConfig",
    "base",
    "crispy_forms",
    "crispy_bootstrap5",
]

ASGI_APPLICATION = "core.asgi.application"

# ─── Channels ─────────────────────────────────────────────────────────────────
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

# ─── Middleware ───────────────────────────────────────────────────────────────
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = "core.urls"

# ─── Templates ────────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "base.utils.global_data",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# ─── Auth ─────────────────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LOGIN_URL = "Base:login"

# ─── Internationalisation ─────────────────────────────────────────────────────
LANGUAGE_CODE = "ar"
LANGUAGES = [("ar", "Arabic"), ("en", "English")]
TIME_ZONE = "Asia/Riyadh"
USE_I18N = True
USE_TZ = True

# ─── Static & Media ───────────────────────────────────────────────────────────
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ─── Jazzmin ──────────────────────────────────────────────────────────────────
JAZZMIN_SETTINGS = {}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": True,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": True,
    "sidebar_nav_flat_style": True,
    "theme": "cyborg",
    "default_theme_mode": "auto",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
    "actions_sticky_top": False,
}

# ─── Crispy Forms ─────────────────────────────────────────────────────────────
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# ─── Celery ───────────────────────────────────────────────────────────────────
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0")
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# ─── Cache ────────────────────────────────────────────────────────────────────
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-session-id",
    }
}

# ─── Payment (Stripe) ─────────────────────────────────────────────────────────
PAYMENT_PUBLIC_KEY = os.getenv("PAYMENT_PUBLIC_KEY")
PAYMENT_SECRET_KEY = os.getenv("PAYMENT_SECRET_KEY")

# ─── Email (configured per environment) ───────────────────────────────────────
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASS")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ─── Cloudflare R2 / S3 ───────────────────────────────────────────────────────
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL")
AWS_S3_CUSTOM_DOMAIN = os.getenv("AWS_S3_CUSTOM_DOMAIN")
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
AWS_QUERYSTRING_AUTH = False
AWS_DEFAULT_ACL = None

# ─── Logging ──────────────────────────────────────────────────────────────────
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name} — {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "app_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "app.log",
            "maxBytes": 5 * 1024 * 1024,   # 5 MB
            "backupCount": 3,
            "formatter": "verbose",
            "encoding": "utf-8",
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "errors.log",
            "maxBytes": 5 * 1024 * 1024,   # 5 MB
            "backupCount": 5,
            "formatter": "verbose",
            "level": "ERROR",
            "encoding": "utf-8",
        },
    },
    "loggers": {
        # Django errors → ملف الأخطاء
        "django.request": {
            "handlers": ["error_file", "console"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.security": {
            "handlers": ["error_file"],
            "level": "ERROR",
            "propagate": False,
        },
        # تطبيقات المشروع → ملف التطبيق
        "Client": {
            "handlers": ["app_file", "console"],
            "level": "WARNING",
            "propagate": False,
        },
        "Engineer": {
            "handlers": ["app_file", "console"],
            "level": "WARNING",
            "propagate": False,
        },
        "Visits": {
            "handlers": ["app_file", "console"],
            "level": "WARNING",
            "propagate": False,
        },
        "Admin": {
            "handlers": ["app_file", "console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}
