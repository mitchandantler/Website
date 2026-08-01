"""Production settings.

Deployed behind Cloudflare + Nginx per
docs/phase-00-foundation/07-deployment.md — Cloudflare terminates TLS and
forwards to the application server, so SECURE_PROXY_SSL_HEADER is required
for Django to correctly detect HTTPS requests.
"""

from .base import *  # noqa: F401,F403
from .base import STORAGES, env

DEBUG = False
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# Cache-busted, compressed static files — requires collectstatic to have run.
STORAGES["staticfiles"] = {
    "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
}

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
