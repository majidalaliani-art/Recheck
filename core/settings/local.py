"""
Local development settings.
Usage: python manage.py runserver  (default)
"""

from .base import *

# ─── Debug ────────────────────────────────────────────────────────────────────
DEBUG = True
ALLOWED_HOSTS = ["*"]

# ─── Database — SQLite local ──────────────────────────────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ─── Storage — local filesystem (no S3 needed) ────────────────────────────────
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# ─── Email — prints to terminal (no SMTP config needed) ───────────────────────
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# ─── Logging — show everything in console during development ──────────────────
LOGGING["loggers"]["Client"]["level"] = "DEBUG"
LOGGING["loggers"]["Engineer"]["level"] = "DEBUG"
LOGGING["loggers"]["Visits"]["level"] = "DEBUG"
LOGGING["loggers"]["Admin"]["level"] = "DEBUG"
