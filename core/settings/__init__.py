"""
Settings package for core.
Local development: core.settings.local
Production:        core.settings.production
"""
import os

env = os.getenv("DJANGO_SETTINGS_MODULE", "")
# Auto-detect production environment
if (
    "production" in env
    or os.getenv("ENVIRONMENT") == "production"
    or os.getenv("DJANGO_ENV") == "production"
    or os.path.exists("/var/www/moon")
):
    from .production import *
else:
    from .local import *

