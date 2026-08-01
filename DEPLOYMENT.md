# Deployment Guide — Mitch & Antler Platform

**This is a living document.** Every time a change is made that affects how
the app is deployed or configured in production — a new environment
variable, a new dependency, a new integration/API key, a new migration that
needs data seeding, a new background service — this file must be updated in
the same change. Do not let this drift out of date.

For the high-level deployment *standards* and philosophy (environments,
hosting architecture, rollback strategy), see
`docs/phase-00-foundation/07-deployment.md`. This file is the concrete,
step-by-step, always-current checklist for actually doing it.

Last updated: 2026-08-01 — after diagnosing the first real Render deploy
failure and adding §1a (Actual Hosting: Render) below.
(Module 7, Careers, was deliberately skipped for now.)

---

## 1. Target Architecture

```
Visitors → Cloudflare (DNS, CDN, TLS) → Crazy Domains (registrar)
         → Linux VPS (Ubuntu LTS) → Nginx → Gunicorn → Django → PostgreSQL
```

Domain: `mitchandantler.com`

**This was the original plan from `docs/phase-00-foundation/07-deployment.md`.
The site is actually being deployed to Render (a managed PaaS) instead — see
§1a below, which is the one that matters day-to-day. Sections 2–9 below
describe the VPS approach and are kept for reference/a possible future
migration; they don't apply to the current Render deploy.**

---

## 1a. Actual Hosting: Render

Repo: `https://github.com/mitchandantler/Website` (GitHub → auto-deploys to
Render on push to `main`).

### Required environment variables (Render dashboard → service → Environment)

| Variable | Value |
|---|---|
| `DJANGO_SETTINGS_MODULE` | `config.settings.production` — recommended for clarity, but **`manage.py` now auto-detects Render via the `RENDER=true` variable Render sets on every service automatically, and defaults to production settings even if this isn't set explicitly** (added after this env var failed to take effect on a second deploy attempt — root cause of that second failure was never confirmed, this is a safety net either way) |
| `SECRET_KEY` | A real generated key — `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`. Never reuse the local dev key from `.env` |
| `ALLOWED_HOSTS` | Your Render subdomain (e.g. `mitchandantler.onrender.com`) plus `mitchandantler.com,www.mitchandantler.com` once DNS is pointed here. No default — will crash on startup if unset |
| `DATABASE_URL` | A Render PostgreSQL instance's connection string (Render can provision one — add a Postgres service and Render usually injects this automatically if linked). **Without this it silently falls back to SQLite** (via the default in `config/settings/base.py`), which loses all data on every redeploy on Render's ephemeral filesystem — do not leave this unset. **Confirmed missing as of 2026-08-01** — see §1b for the fix plus the one-time local→Render data migration this made necessary |
| `TIME_ZONE` | `Australia/Sydney` (optional, that's already the default) |
| `RESEND_API_KEY`, `DEFAULT_FROM_EMAIL`, `CONTACT_NOTIFICATION_EMAIL` | For the Contact form email — see §3 below for what happens if left blank |

### Build Command

```
pip install -r requirements/production.txt && python manage.py migrate && python manage.py collectstatic --no-input
```

No `npm` step needed — **Render's native Python build environment has no
Node.js**, so the compiled `static/css/tailwind.css` is committed straight
to the repo instead of being built during deploy (see `.gitignore` —
`static/css/tailwind.css` is deliberately *not* ignored, unlike
`node_modules/`). **Whenever you change a template or `static/css/input.css`
locally, run `npm run build:css` and commit the updated
`static/css/tailwind.css` before pushing** — otherwise Render will deploy
stale CSS.

### Start Command

```
gunicorn config.wsgi:application
```

### Python version

Render defaults to the newest available Python (3.14.3 as of 2026-08-01)
unless told otherwise, which is untested against this project (developed
and tested on 3.13.2). A `.python-version` file in the repo root pins this
to `3.13.2` — Render respects this automatically, no separate dashboard
setting needed.

### Troubleshooting checklist for a failed Render build

- `ModuleNotFoundError: No module named 'debug_toolbar'` → should no longer happen at all now that `manage.py` auto-detects Render via `RENDER=true` (see above) and forces production settings regardless of `DJANGO_SETTINGS_MODULE`. If it somehow still happens, double-check Render is actually setting `RENDER=true` (it should, automatically, on every service) — verify under the service's Environment tab
- `ImproperlyConfigured: ... ALLOWED_HOSTS` → that env var isn't set
- Site loads but completely unstyled → `static/css/tailwind.css` wasn't committed/up to date, or `collectstatic` didn't run
- Data disappears after a redeploy → `DATABASE_URL` isn't set (site silently fell back to ephemeral SQLite)
- Local admin content doesn't match live site → local and Render have always been separate databases; see §1b for the one-time migration
- Uploaded images (hero, menu, gallery, promotions) don't display at all in production, even after §1b's data migration → **root cause found 2026-08-01, in two parts**: (1) `config/urls.py` only served `MEDIA_URL` when `settings.DEBUG` was `True`. (2) The first fix attempt (just removing our own `if settings.DEBUG` wrapper around `django.conf.urls.static.static()`) **did not work** — that helper has its own internal `if not settings.DEBUG: return []` guard baked into Django itself (see `django/conf/urls/static.py`), so it silently no-op'd in production no matter how it was called. Real fix: register `django.views.static.serve` directly via `re_path()`, bypassing the helper entirely (see `config/urls.py`) — verified locally under simulated production settings (`DEBUG=False`): `GET /media/hero/HeroPhoto.jpg` → `200 image/jpeg`. Acceptable for this site's traffic level since there's no S3/R2/CDN for media yet; revisit if traffic grows. The 16 real image files (~7MB) were also force-added to git (`git add -f media/...`) since `.gitignore` normally excludes `/media/*` and Render has no other way to receive them. **This does not solve future uploads** — any new image uploaded via the live `/admin/` after this still lands on Render's ephemeral disk and vanishes on the next redeploy; that's the same unresolved persistent-storage decision flagged in §1b Step 4

---

## 1b. One-Time Data Migration: Local → Render Postgres

**Why this exists:** as of 2026-08-01, Render had no `DATABASE_URL` set, so the
live site was silently running on ephemeral SQLite (or possibly not
persisting at all across redeploys) — a completely separate database from
the local one used for all development/testing. This is why the local admin
and the live Render admin never matched: the real 45-item menu, About Us
story, promotions, gallery, opening hours, socials, etc. only ever existed
locally. This section is a one-time fix to get that content onto a real,
persistent Render Postgres database.

### Step 1 — Provision Postgres on Render

1. Render Dashboard → **New → PostgreSQL**, same region as the web service.
2. Render's free Postgres tier is **only free for 90 days**, then it's
   deleted unless upgraded to a paid plan — don't put this off indefinitely
   once real customer/menu data is in it.
3. Copy the **Internal Database URL** it gives you.
4. Web service → **Environment** tab → add `DATABASE_URL` = that internal
   connection string. This alone fixes the "not persisting" problem going
   forward, even before any data migration.

### Step 2 — Export local content

```
./scripts/export_local_data.sh
```

Writes `data/production_seed.json` (a Django fixture). Deliberately
excludes `auth`/`sessions`/`contenttypes`/`admin.logentry` (the Render
superuser is created/reset separately — see §8) and
`contact.contactsubmission` (real test submissions from local dev, not site
content — don't copy fake "customers" into production). As of this export:
80 records — 1 `SiteSetting`, 1 `Socials`, 7 `OpeningHours`, 8
`GalleryImage`, 8 `DietaryTag`, 5 `MenuCategory`, 45 `MenuItem`, 2
`Promotion`, 1 `AboutPageContent`, 1 `HeroImage`, 1 `HomePageContent`.

Commit and push `data/production_seed.json` so Render's build has access to
it (Render deploys from the git repo, there's no other way to get a file
onto it without a paid Shell tab).

### Step 3 — Load it into Render Postgres (temporary Build Command edit)

Web service → **Settings → Build Command**, temporarily change to:

```
pip install -r requirements/production.txt && python manage.py migrate && python manage.py loaddata data/production_seed.json && python manage.py collectstatic --no-input
```

Trigger a manual deploy. **As soon as it succeeds, revert the Build Command
back to the normal version** (without the `loaddata` step) and redeploy
again:

```
pip install -r requirements/production.txt && python manage.py migrate && python manage.py collectstatic --no-input
```

This matters — `loaddata` is not something to leave running on every
deploy. It overwrites rows by primary key on every run, so if it stayed in
the Build Command, any edits made afterward through Render's live `/admin/`
would get silently reverted back to this local snapshot on the next push.
It's a one-time seed, not an ongoing sync.

### Step 4 — Media files (images) need separate handling

`dumpdata`/`loaddata` only moves database rows — `MenuItem.image`,
`GalleryImage.image`, `Promotion.image`, and `HeroImage.image` fields will
point at file paths that don't physically exist on Render yet (local
`media/` is `.gitignore`d, not committed). As of this writing that's 16
files, ~7MB total. Two options:

- **Re-upload manually** through Render's live `/admin/` after the data
  load — only 16 files, probably the least error-prone option.
- **Commit `media/` temporarily** (bypass `.gitignore`, push, then decide
  whether to keep it tracked or remove it once confirmed working).

**Bigger unresolved issue, flagging rather than fixing now:** Render's free
web-service tier has an *ephemeral filesystem* — even after this migration,
any new image uploaded through the live admin will vanish on the next
redeploy, indefinitely, until this is addressed properly. The real fix is
external persistent storage (e.g. Cloudflare R2 or S3 via
`django-storages`) or Render's paid persistent-disk add-on. That's a
bigger, separately-costed decision — not bundled into this fix.

---

## 2. Prerequisites (one-time, before first deploy)

- [ ] Linux VPS provisioned — Ubuntu LTS, 2 vCPU / 4 GB RAM / 40–80 GB SSD minimum
- [ ] Node.js + npm installed on the server (build-time only — used to compile Tailwind CSS, not run at request time)
- [ ] PostgreSQL installed on the server (or a managed Postgres instance)
- [ ] Domain `mitchandantler.com` pointed at the server via Cloudflare DNS
- [ ] Cloudflare SSL/TLS mode set to **Full (Strict)**
- [ ] A dedicated deploy user on the server (not root)
- [ ] SSH key access configured for deployment
- [ ] Resend account + API key (for Contact form emails — see Module Log below)

---

## 3. Environment Variables

Copy `.env.example` to `.env` on the server and fill in real production
values. **Never commit `.env`.**

| Variable | Required in prod? | Notes |
|---|---|---|
| `SECRET_KEY` | Yes | Generate a fresh one for production — never reuse the dev key. `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | Yes | Must be `False` in production |
| `ALLOWED_HOSTS` | Yes | e.g. `mitchandantler.com,www.mitchandantler.com` |
| `DATABASE_URL` | Yes | PostgreSQL connection string, e.g. `postgres://user:pass@localhost:5432/mitchandantler` |
| `TIME_ZONE` | No | Defaults to `Australia/Sydney` |
| `DJANGO_SETTINGS_MODULE` | Yes | Set to `config.settings.production` (see §6) |
| `RESEND_API_KEY` | Yes | If unset, contact form submissions still save but no notification email is sent (logged, not an error) — see Module Log |
| `DEFAULT_FROM_EMAIL` | Yes | The "from" address for Resend notification emails |
| `CONTACT_NOTIFICATION_EMAIL` | Yes | Where contact form submissions are sent |

> Whenever a new setting is added to `config/settings/*.py`, add a row here.

---

## 4. Server Setup (one-time)

```bash
# System packages
sudo apt update && sudo apt install -y python3.13 python3.13-venv \
    postgresql nginx git nodejs npm

# Database
sudo -u postgres createuser mitchandantler
sudo -u postgres createdb mitchandantler --owner=mitchandantler
sudo -u postgres psql -c "ALTER USER mitchandantler WITH PASSWORD '<strong-password>';"

# App directory
sudo mkdir -p /srv/mitchandantler
sudo chown $USER:$USER /srv/mitchandantler
git clone <repo-url> /srv/mitchandantler
cd /srv/mitchandantler

# Python environment
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements/production.txt

# Frontend build (Tailwind CSS)
npm ci
npm run build:css

# Environment file
cp .env.example .env
# edit .env with real production values
```

---

## 5. Gunicorn (systemd service)

Create `/etc/systemd/system/mitchandantler.service`:

```ini
[Unit]
Description=Mitch & Antler Django app (Gunicorn)
After=network.target

[Service]
User=<deploy-user>
Group=www-data
WorkingDirectory=/srv/mitchandantler
Environment="DJANGO_SETTINGS_MODULE=config.settings.production"
ExecStart=/srv/mitchandantler/.venv/bin/gunicorn \
    config.wsgi:application \
    --bind 127.0.0.1:8000 \
    --workers 3

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now mitchandantler
```

---

## 6. Nginx

Create `/etc/nginx/sites-available/mitchandantler`:

```nginx
server {
    listen 80;
    server_name mitchandantler.com www.mitchandantler.com;

    location /static/ {
        alias /srv/mitchandantler/staticfiles/;
    }

    location /media/ {
        alias /srv/mitchandantler/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/mitchandantler /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

Cloudflare terminates the public HTTPS connection; Nginx receives plain
HTTP from Cloudflare. `SECURE_PROXY_SSL_HEADER` is already configured in
`config/settings/production.py` so Django correctly detects HTTPS.

---

## 7. Deploy / Release Checklist

Run this every time you deploy a new release:

```bash
cd /srv/mitchandantler
source .venv/bin/activate

git pull origin main
pip install -r requirements/production.txt
npm ci
npm run build:css
python manage.py migrate
python manage.py collectstatic --noinput

sudo systemctl restart mitchandantler
```

Then smoke test:

- [ ] `https://mitchandantler.com/` loads
- [ ] `https://mitchandantler.com/admin/` loads and login works
- [ ] Check `logs/error.log` for anything unexpected
- [ ] `sudo systemctl status mitchandantler` shows active/running

---

## 8. First-Ever Deploy Only

After the very first `migrate` on a fresh production database:

```bash
python manage.py createsuperuser
```

Then log into `/admin/` and fill in the seeded `SiteSetting` row (phone,
email, address, OpenTable/Uber Eats/DoorDash/QR/Maps URLs, social links) and
the real `OpeningHours` for each day — both are seeded as placeholders/closed
by migration and must be filled in with real data before going live.

---

## 9. Rollback

```bash
cd /srv/mitchandantler
git checkout <previous-tag-or-commit>
source .venv/bin/activate
pip install -r requirements/production.txt
python manage.py migrate   # only if the previous version needs a schema rollback
sudo systemctl restart mitchandantler
```

Database migrations are additive by default — check whether a rollback
actually requires reversing a migration before running one blindly.

---

## 10. Module Log

Running log of what each module added that matters for deployment. Update
this whenever a new module ships.

| Module | What it added | Deployment impact |
|---|---|---|
| Module 0 — Project scaffold | Django project, settings split (base/development/staging/production), WhiteNoise, DRF, 8 apps | Baseline `.env` vars: `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `DATABASE_URL`, `TIME_ZONE` |
| Module 1 — Core config | `SiteSetting` (apps/common), `OpeningHours` + `SpecialHoursOverride` (apps/contact) | No new env vars. New data migrations seed 1 `SiteSetting` row + 7 `OpeningHours` rows — must be filled in via `/admin/` post-deploy (see §8) |
| Module 2 — Home + About pages | Base template + header/footer partials, `apps/website` Home/About views, Tailwind CSS build pipeline (`package.json`, `tailwind.config.js`, `static/css/input.css` → `static/css/tailwind.css`), `site_settings`/`opening_hours` context processors, dev-vs-prod static storage split (manifest storage only in production) | **New build step required on every deploy: `npm ci && npm run build:css` before `collectstatic`** (added to §4 and §7 above). Node/npm now a required prerequisite on the server (build-time only, see §2). Static storage backend now differs by environment — production uses WhiteNoise's `CompressedManifestStaticFilesStorage` (requires `collectstatic` to have run), development uses plain `StaticFilesStorage` |
| Module 3 — Menu | `DietaryTag`, `MenuCategory`, `MenuItem` models + admin (apps/menu), Menu page at `/menu/`, `MenuItem.image` uploads to `media/menu/<food\|drink>/` | No new env vars. No seed data — menu content is entered by staff via `/admin/` (Menu Categories → Menu Items) after deploy. First deploy of this module needs at least one active `MenuCategory` + available `MenuItem` before the Menu page shows anything other than "Menu coming soon" |
| Module 4 — Gallery | `GalleryImage` model + admin (apps/gallery), Gallery page at `/gallery/` with an Alpine.js lightbox, images upload to `media/gallery/`. Also fixed a latent bug from Module 2: added the missing `[x-cloak]{display:none}` CSS rule (`static/css/input.css`) — without it, `x-cloak` elements (mobile nav, lightbox) could flash visible before Alpine.js initializes | No new env vars. No seed data — gallery images are uploaded by staff via `/admin/` after deploy. Confirm `MEDIA_ROOT`/`MEDIA_URL` are actually served in production (Nginx `location /media/` block, §6) since this is the first module with user-uploaded content actually displayed on a public page |
| Module 5 — Offers/Promotions | `Promotion` model + admin (apps/promotions), Offers page at `/offers/`, featured-offers section on Home (top 3 currently-active), images upload to `media/promotions/`. `Promotion.objects.currently_active()` filters on `is_active` + `start_date`/`end_date` against **server local date** (`timezone.localdate()`) | No new env vars. No seed data. **Correctness depends on the server's configured `TIME_ZONE`** (`Australia/Sydney` by default, see §3) — if that's ever wrong, promotions will expire/activate at the wrong moment. No cron/scheduled job needed: expiry is computed live on every request, not by a background task |
| Module 5 revision — date-order validation + Offers renamed to Promotions | **Root cause of a reported "admin doesn't sync with website" issue**: a real `Promotion` ("Birthday Promotion") had `start_date` (Sep 1, 2026) set *after* `end_date` (Aug 3, 2026) — `currently_active()` was filtering correctly, the data was just self-contradictory (started in the future per one field, already ended per the other), so it correctly never appeared. Added `Promotion.clean()` raising a `ValidationError` ("End date must be on or after the start date") the moment start > end — verified it now blocks saving that exact bad combination via the real admin form. Also renamed all **website-visible** "Offers" text to "Promotions" (nav, page `<title>`/`<h1>`, Home section heading/link) to match the admin's naming and reduce this confusion recurring — URL path (`/offers/`), url name (`promotions:offers`), view class (`OffersView`), and template filename were deliberately left unchanged to keep the change low-risk/scoped | No migration (`clean()` is Python-level validation only, not a DB constraint — the existing bad row still needs the user to fix it via `/admin/`, which will now be enforced on save). No env vars |
| Module 5 revision — Promotion admin edit link + column clarity | `PromotionAdmin` had no `list_display_links` set, so Django defaulted to making only the `thumbnail` column (an image, or a plain "—" dash when no image is uploaded) the clickable edit link — easy to miss, reported as "no edit option". Added `list_display_links = ("title",)` so the title text is now the obvious clickable link (verified: renders as a real `<a href=".../change/">` in the changelist). Also renamed the computed `currently_active` column's label from "Currently Active" to **"Live on Website"** to visually distinguish it from the real `is_active` field/checkbox — they can disagree by design (e.g. `is_active=True` but dates not yet reached shows "Live on Website: No"), which was being misread as a bug | No migration, no env vars. Verified against real data: "another promotion" correctly shows Active=Yes / Live on Website=No since it doesn't start until tomorrow |
| Module 6 — Reviews + FAQ | `Review` + `FAQItem` models + admin (apps/website), Reviews page at `/reviews/`, FAQ page at `/faq/` (Alpine.js accordion), featured-reviews section on Home (top 3 `is_active` + `is_featured`) | No new env vars, no seed data, no new dependencies. Reviews are entered manually via `/admin/` (no live Google Reviews integration — that's an explicit future consideration per `docs/phase-01-website/07-integrations.md`, not built) |
| Module 8 — Contact form + Resend | `ContactSubmission` model + read-only admin (apps/contact, no manual add — only created via the public form), `ContactForm`, `apps/contact/services.py` sends a notification via the Resend SDK (`resend.Emails.send`) on submission, Contact page at `/contact/` (form + address/phone/email/map/hours), global Django-messages banner added to `base.html` | **`RESEND_API_KEY`, `DEFAULT_FROM_EMAIL`, `CONTACT_NOTIFICATION_EMAIL` now actually load-bearing** (env table above updated from "once shipped" to required). If `RESEND_API_KEY` is blank, the submission still saves and the skip is logged — confirmed by testing with it unset locally. No seed data |

| Module 9 — Booking + Order Online | `BookingView` + `OrderOnlineView` (apps/booking, no new models — both pages just read existing `SiteSetting` fields), `/booking/` embeds `opentable_embed_url` as an iframe with a phone/contact fallback if blank, `/order-online/` lists whichever of `qr_ordering_url`/`uber_eats_url`/`doordash_url` are set, with the same phone fallback if none are | No new env vars, no migrations, no new dependencies. **Content-only rollout**: staff already populated `SiteSetting` (phone, email, address, Google Maps link, and a real booking URL) via `/admin/` before this module even shipped — Uber Eats/DoorDash/QR links are still blank and will show the phone fallback until staff add them |

| Module 10 — SEO polish | `django.contrib.sitemaps` added to `INSTALLED_APPS`; `/sitemap.xml` and `/robots.txt` (dynamic, built from `reverse()` — no hardcoded domain); `canonical_url` context processor + `<link rel="canonical">`; minimal Open Graph (`og:type`/`og:site_name`/`og:url`) + `twitter:card` in `base.html` (og:title/description deliberately omitted — crawlers fall back to `<title>`/meta description, avoiding per-page duplication); schema.org JSON-LD: Restaurant (Home + Contact, includes `aggregateRating` only when active reviews exist), FAQPage (FAQ page, only when FAQ items exist), Menu (Menu page, only when items exist, hardcodes `priceCurrency: AUD`); custom `templates/404.html` | No new env vars, no migrations. New shared helper `apps/common/schema.py` (`build_local_business_schema`, `to_json_ld`) — reuse it for any future page needing schema.org markup rather than hand-rolling JSON-LD again. `AUD` currency assumption should be revisited if the business ever expands beyond Australia |

| Module 9 revision — Order Online UI + URL capacity | `/order-online/` changed from stacked link cards to a `<select>` dropdown (Alpine.js `x-model`) + "Continue to Order" button; `SiteSetting.uber_eats_url`/`doordash_url`/`qr_ordering_url` widened from Django's default 200-char `URLField` to `max_length=350` | New migration (`common.0003_alter_sitesetting_...`) — non-destructive field-length change, safe to run on existing data. Verified a 326-char URL round-trips correctly. No env var or dependency changes |
| Module 9 revision — Order Online nav hover dropdown | Header nav's "Order Online" button (desktop only — mobile keeps a plain link, hover doesn't apply on touch) now shows a hover dropdown listing whichever of Pickup/Uber Eats/DoorDash are configured, each linking to `/order-online/?method=<pickup\|ubereats\|doordash>`. `OrderOnlineView` reads that `method` query param and pre-selects the matching option in the page's `<select>`, falling back to the first configured option if the param is missing/invalid. `ordering_options` gained a stable `key` field for this matching (previously only `label`/`url`) | No migration, no env vars. Verified against the real, now fully-configured ordering links (Chewzie pickup, Uber Eats, DoorDash) — all three nav dropdown links correctly pre-select their option, including the very long Uber Eats URL (a good real-world exercise of the 350-char field above) |
| Module 1 revision — Opening Hours data fix | Fixed real data: all 7 `OpeningHours` rows had real times entered via `/admin/` but `is_closed=True` was still set from the Module 1 seed placeholder, silently overriding the times and showing "Closed" every day. `OpeningHoursAdmin` now has `list_editable` on open/close/is_closed (edit all 7 days on one screen) plus clearer `help_text` on `is_closed` explaining it overrides the times | New migration (`contact.0004_...`, help_text only, no schema change). No env vars. **Operational note:** if hours ever look wrong again on the site, check `is_closed` on the relevant `OpeningHours` row first — it silently wins over open_time/close_time |
| Module 1 revision — Opening Hours display consolidated to footer only | The full 7-day `OpeningHours` table (via `components/opening_hours_table.html`, already backed by the `opening_hours` context processor — no view changes needed) removed from Home and Contact pages, added as a new "Service Hours" 4th column in `partials/footer.html` (grid widened `sm:grid-cols-3` → `sm:grid-cols-2 lg:grid-cols-4`) so it now shows site-wide instead of on 2 specific pages. Contact page's hours section replaced with a **static** one-line "Contact Hours: Mon–Sun: 6:00am – 2:00pm" — this text is hardcoded per explicit user request, not sourced from `OpeningHours`, so it will silently go stale if real hours ever change and won't need a migration to fix, just a template edit | No migration, no env vars. **Operational note:** the footer's "Service Hours" is the only remaining live admin-driven hours display — the Contact page text is now a separate, manually-maintained duplicate that needs updating by hand if hours change |
| Module 1 revision — Footer Service Hours condensed | New `apps/contact/context_processors.py:service_hours_summary` — when every `OpeningHours` day shares identical open/close times (today's real case: all 7 days 6:30 AM–2:00 PM), the footer shows one line, `"Mon-Sun 6:30 AM - 2 PM"`, instead of a 7-row table. **Deliberately NOT hardcoded** (unlike the Contact page line above) — if any day is ever closed or has different hours, it automatically falls back to the full per-day table instead of showing a wrong summary. Verified both paths: temporarily marked Sunday closed → table reappeared; restored → condensed line came back | New context processor registered in `config/settings/base.py` (no migration, no env vars). Time formatting is custom (`6:30 AM`, `2 PM` — no leading zero, minutes dropped on the hour) since Django's default locale format uses lowercase `a.m./p.m.` |
| Module 1 revision — TikTok field + icon-based social links | Added `SiteSetting.tiktok_url` (same pattern as `instagram_url`/`facebook_url`, in the "Social Links" admin fieldset). Footer's "Connect" column now shows actual icons (inline SVG, no new dependency) for Instagram/Facebook/TikTok instead of plain text links — each only rendered if its URL is configured, `aria-label`ed for accessibility since they're icon-only | New migration (`common.0006_sitesetting_tiktok_url`). No env vars, no new dependency (hand-written inline SVGs, not an icon library/font). Verified against real Instagram/Facebook URLs already in `SiteSetting`, plus a temporary TikTok value to confirm that icon path too |
| Module 2 revision — Google Maps embed fix | `SiteSetting.google_maps_iframe_src` property added: only returns the stored `google_maps_embed_url` if it actually contains `/maps/embed` (a real Google "Share > Embed a map" URL); otherwise returns empty so no broken iframe is rendered. `about.html`/`contact.html` now use this property for the iframe `src`, plus always show a separate "View on Google Maps" link using the raw stored URL (works with any Google Maps URL type, including share links) | New migration (`common.0005_...`, help_text only). **Root cause**: a `maps.app.goo.gl` share link was stored in `google_maps_embed_url` — Google returns `X-Frame-Options: SAMEORIGIN` for those, causing "refused to connect" when framed. **A commonly-cited free workaround (`maps.google.com/maps?q=...&output=embed`, no API key) was tested directly against Google and confirmed dead (404) as of 2026-07-31** — don't reintroduce it. The only remaining no-API-key fix is manually obtaining a real `/maps/embed` URL from Google Maps' own Share dialog (help_text on the field explains the steps); the alternative is a paid/free-tier Google Maps Embed API key, not set up |
| Module 2 revision — Home page hero admin management | `HomePageContent` (singleton, same pattern as `SiteSetting`) + `HeroImage` (ordered, `is_active`, like `GalleryImage`) added to apps/website; Home hero heading/subheading and 0+ rotating hero images now editable via `/admin/` instead of hardcoded in `home.html`. Zero active images falls back to the original plain-background hero (no broken/empty state); 2+ images auto-rotate every 5s via Alpine, with white text applied over images for contrast | New migrations: `website.0002_...` (schema) + `website.0003_seed_home_page_content` (seeds 1 `HomePageContent` row with the same copy that used to be hardcoded, so nothing visually changes until edited). No env vars. Hero images upload to `media/hero/` |
| Module 3 revision — Menu CSV bulk import + requested categories | Seeded 5 `MenuCategory` rows the user specifically requested (All Day Menu, Little Ones — food; Coffee and Frappes, Cold Beverages, Cold Drinks — drink), non-destructively (existing "All Day Menu" category + its real item were left untouched). New CSV bulk-import feature on `/admin/menu/menuitem/` — an "Import CSV" button opens a custom admin view (`apps/menu/services.py:import_menu_csv`, `apps/menu/forms.py`) that upserts `MenuItem`s by (category, name): matching rows are updated, new ones created, invalid rows (unknown category, bad price) are reported per-row without blocking the rest of the file. Re-uploading an edited CSV is always safe (no duplicates) | New migration (`menu.0002_seed_menu_categories`, data-only). No env vars, no new dependencies (CSV parsing uses Python's stdlib `csv` module, not a third-party import library — kept deliberately lightweight per user's explicit request to scope this to the Menu module only). **Note for the future**: true AI/OCR-based PDF or photo menu parsing was discussed and explicitly deferred — this CSV import is the reliable alternative that was built instead |
| Module 3 revision — Menu Item approval workflow | `MenuItem.is_approved` field added (default `True` for normal manual admin entry, so existing items are unaffected). `import_menu_csv` now forces `is_approved=False` on every row it creates *or* updates — CSV-driven changes never go live automatically. `MenuItemAdmin` gained an `is_approved` column/filter/inline-edit plus a bulk "Approve selected menu items" action. The public `/menu/` page (`MenuView`) now only shows items where both `is_available=True` and `is_approved=True` — Django Admin is the single source of truth for what's live; nothing reaches the website without a staff member reviewing it there | New migration (`menu.0003_menuitem_is_approved`, additive/non-destructive — existing rows default to approved). No env vars. **Workflow going forward**: after any CSV import, filter Menu Items by "Is approved: No", review each row (price, description, and especially dietary tags), then select and use "Approve selected menu items" to publish |
| Module 3 revision — CSV import encoding crash fix | Fixed a real `UnicodeDecodeError` (500 error) hit importing a real CSV — Excel/Numbers exports are usually Windows-1252, not strict UTF-8, and any "smart quote"/em-dash breaks a naive UTF-8 decode. `import_menu_csv` now tries `utf-8-sig` → `cp1252` → `latin-1` (guaranteed to succeed) in order, and separately sniffs magic-number prefixes (ZIP/PDF/JPEG/PNG) to give a specific friendly error if someone uploads an actual .xlsx or the menu PDF/photo itself instead of a CSV, rather than a decode crash | No migration, no env vars, no new dependency. Verified against a real cp1252-encoded curly-apostrophe CSV (the exact failure mode reported) and a fake .xlsx upload — both now handled gracefully |
| Module 3 revision — Menu page horizontal tabs | `/menu/` changed from a long stacked scroll (Food heading → categories → Drinks heading → categories) to horizontal pill-style tab buttons, one per category with items (Alpine.js `x-show`/`active` state, category id as the key) — clicking a tab shows only that category's items, no more scrolling through the whole menu. `MenuView` now builds one pre-filtered `categories` list (empty categories excluded, so no dead-end tabs) instead of separate `food_categories`/`drink_categories`; `menu_category_section.html` no longer renders its own category-name heading since the tab label already shows it | No migration, no env vars. Verified against the real 45-item, 5-category live menu — all 5 tabs render in the correct order with "All Day Menu" active by default, and the Menu schema.org JSON-LD (used for SEO) still reports all 5 sections/45 items correctly |

| Module 2 revision — Visible no-map fallback | On About and Contact, when `google_maps_iframe_src` is empty (current real state — the stored URL is still a `maps.app.goo.gl` share link, not a real `/maps/embed` URL), the "View on Google Maps" link used to render as small unstyled inline text with nothing else around it — reported as "I do not see anything below Google". Changed to a proper `aspect-video` placeholder box (same footprint the real map would occupy) with a clear button-styled link inside, so the map area is always visibly present even before a real embed URL is set | No migration, no env vars. This does not fix the underlying "no real map embed" issue (still needs a `/maps/embed` URL from Google's own Share dialog, per the Module 2 Google Maps fix above) — it only makes the interim fallback state look intentional instead of broken/empty |

| Module 1 revision — Site Settings admin fieldsets clarified | User reported "Social media, order online items are not visible" in `/admin/` — fields were all present and functional (verified via test client) but buried under a vague "Integrations" fieldset with no mention of "Order Online" anywhere, and "Social Links" (not "Social Media"). Split into 5 clearly-named fieldsets: Contact Details, Google Maps, Booking, **Order Online** (`uber_eats_url`/`doordash_url`/`qr_ordering_url`), **Social Media** (`instagram_url`/`facebook_url`/`tiktok_url`) — verified each label renders on the change form | No migration (fieldset labels only, no schema/model change), no env vars |

| Module 1 revision — Socials moved to its own model/admin entry | Fieldset renaming wasn't enough — user wanted socials fully out of Site Settings. Added `Socials` (new singleton model, same save()/load()/delete()-noop pattern as `SiteSetting`), registered as its own `SocialsAdmin` — shows as a separate "Socials" row on the admin index, independent of "Site Settings". New `apps.common.context_processors.socials` makes it available site-wide; `footer.html`'s icon links now read `socials.instagram_url`/`facebook_url`/`tiktok_url` instead of `site_settings.*` | New migration (`common.0007_...`) removes `instagram_url`/`facebook_url`/`tiktok_url` from `SiteSetting` and creates `Socials` — **includes a `RunPython` data-copy step that runs between the create and remove operations**, carrying over the real Instagram/Facebook URLs that already existed before they'd have been dropped. Verified post-migration: both real URLs present on the new `Socials` row, footer icons still render them correctly, `SiteSetting`'s form no longer shows social fields at all |

| Module 1 revision — Admin index reordered | New `apps/common/admin_ordering.py`, loaded via `CommonConfig.ready()` — patches `AdminSite.get_app_list` to a fixed order (Common → Website → Menu → Gallery → Promotions → Contact → Booking → Dashboard → Auth) instead of Django's default alphabetical order, which buried day-to-day sections under "Authentication and Authorization". Verified: "Common" (Site Settings, Socials) now shows first, Auth last | No migration, no env vars. If a new app is added later and doesn't appear in `APP_ORDER`, it just sorts to the end (not lost) — add it to the list for a specific position |
| Module 2 revision — About page admin-editable | `AboutPageContent` (singleton, same pattern as `HomePageContent`) added to apps/website — heading + full story text now editable via `/admin/` instead of hardcoded in `about.html`. Seeded with the exact real story text already live, so nothing changed visually. Story is stored as one `TextField` (paragraphs separated by blank lines) and rendered with Django's `linebreaks` filter, which also handles HTML-escaping automatically — do **not** pre-escape `&`/etc. when editing the default/seed text in Python | New migration (`website.0004_aboutpagecontent`, seeds via the model's `default=` value, no separate data migration needed since this is a new model, not a data move). No env vars. Verified an admin edit actually changes the live page, then restored |
| Infra — Admin "Forgotten your login credentials?" self-service reset | Root cause of the recurring "reset the Render superuser password" requests: the free web-service tier has no Shell tab, so every reset needed a temporary Build/Start Command hack. Fixed properly instead: added the 4 standard Django auth URLs (`admin_password_reset`, `password_reset_done`, `password_reset_confirm`, `password_reset_complete`) to `config/urls.py` before the `admin/` include — Django's own admin login template already shows a reset link automatically once `admin_password_reset` resolves, no custom template needed (confirmed via `.venv`'s shipped `admin/templates/registration/*` — all needed templates ship with `django.contrib.admin`/`django.contrib.auth`, nothing to add). `EMAIL_BACKEND` in `config/settings/base.py` now points at **Resend's SMTP relay** (`smtp.resend.com:587`, user `resend`, password = the existing `RESEND_API_KEY`) so this reuses the same provider as Contact form notifications — no new env var needed. `development.py`'s console `EMAIL_BACKEND` override is untouched, so local testing still just prints the email instead of sending it | No migration. No new env vars — reuses `RESEND_API_KEY`/`DEFAULT_FROM_EMAIL`, both already required (see §1a). Verified end-to-end locally: submitted the reset form, generated a real token, followed the confirm link, set a new password, logged in with it, then restored the original local password. **On Render, this only works once `RESEND_API_KEY` is a real (not blank) value** — same requirement the Contact form already has |

_(Module 11, testing pass, is next. Module 7, Careers, remains deferred —
see project memory.)_
