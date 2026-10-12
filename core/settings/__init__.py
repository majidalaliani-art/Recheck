"""
Settings package for core.
Local development: core.settings.local
Production:        core.settings.production
"""

# Default to local settings when core.settings is loaded directly
from .local import *
