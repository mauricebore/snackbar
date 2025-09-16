import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------
# STATIC FILES CONFIGURATION
# ---------------------------

STATIC_URL = '/static/'

# Where Django will collect static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Extra places Django will look for static files (optional, if you have a /static folder in apps)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Use Whitenoise to serve static files in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ---------------------------
# MIDDLEWARE
# ---------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # <- ADD THIS LINE
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ---------------------------
# OTHER IMPORTANT SETTINGS
# ---------------------------

# Ensure DEBUG = False on Render
DEBUG = False

# Add your Render domain here
ALLOWED_HOSTS = ["snackbar-3.onrender.com", "127.0.0.1", "localhost"]

