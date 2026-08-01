"""Staging settings — mirrors production as closely as practical.

Per docs/phase-00-foundation/07-deployment.md, staging exists to test final
release candidates against a production-like configuration before release.
"""

from .production import *  # noqa: F401,F403
