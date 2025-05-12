from os import getenv, path
from dotenv import load_dotenv
from .base import * #noqa
from .base import BASE_DIR

local_env_path = path.join(BASE_DIR, ".envs", ".env.local")

if path.exists(local_env_path):
    load_dotenv(local_env_path)

SECRET_KEY = getenv("SECRET_KEY")

DEBUG = getenv("DEBUG", "True") == "True"

SITE_NAME = getenv("SITE_NAME")

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

ADMIN_URL = getenv("ADMIN_URL")

EMAIL_BACKEND = 'django_celery_email.backends.CeleryEmailBackend'
EMAIL_HOST = getenv("EMAIL_HOST")
EMAIL_PORT = getenv("EMAIL_PORT")
DEFAULT_FROM_EMAIL = getenv("DEFAULT_FROM_EMAIL")
DOMAIN = getenv("DOMAIN")

MAX_UPLOAD_SIZE = 1 * 1024 * 1024

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://0.0.0.0:8000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://0.0.0.0:8080",
]
LOCKOUT_DURATION = timedelta(minutes=1)
LOGIN_ATTEMPTS = 3
OTP_EXPIRATION = timedelta(minutes=1)
