#!/usr/bin/env bash
set -euo pipefail

# One-time export of local content (menu, promotions, gallery, website pages,
# contact/booking settings, socials, etc.) for import into Render's Postgres
# database once DATABASE_URL is set there. See DEPLOYMENT.md §1b.
#
# Deliberately excludes auth/sessions/contenttypes/admin logs — the Render
# superuser is created/reset separately, not copied from local. Also excludes
# contact.contactsubmission — those are real test submissions from local
# development, not site content, and shouldn't appear as fake "customers" in
# production.

cd "$(dirname "$0")/.."

# Prefer the project's venv (has the right installed packages) over
# whatever "python"/"python3" happens to resolve to on PATH.
PYTHON=".venv/bin/python"
if [ ! -x "$PYTHON" ]; then
  PYTHON=python3
fi

mkdir -p data

"$PYTHON" manage.py dumpdata \
  --natural-foreign --natural-primary \
  --exclude auth \
  --exclude contenttypes \
  --exclude admin.logentry \
  --exclude sessions.session \
  --exclude contact.contactsubmission \
  --indent 2 \
  -o data/production_seed.json

echo "Wrote data/production_seed.json"
