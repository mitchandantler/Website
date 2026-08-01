# Mitch & Antler Platform

Modular Django platform for Mitch & Antler Café. See `docs/` for the full
roadmap and phase documentation — start with `docs/phase-00-foundation/` for
architecture and standards, and `docs/phase-01-website/` for the current
Phase 1 (Public Website) scope.

## Local Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements/development.txt
cp .env.example .env        # then fill in real values
python manage.py migrate
python manage.py createsuperuser

npm install
npm run build:css           # one-off build; use `npm run watch:css` while editing templates

python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the public site and
`http://127.0.0.1:8000/admin/` for the admin.

By default, local development uses SQLite (no setup required). To use
PostgreSQL, set `DATABASE_URL` in `.env` (see `.env.example`).

Styling is Tailwind CSS, compiled from `static/css/input.css` into
`static/css/tailwind.css` (gitignored — always rebuild after pulling
changes). See `DEPLOYMENT.md` for how this fits into deployment.

## Project Structure

Each business feature is its own Django app under `apps/`, per
`docs/phase-00-foundation/03-project-structure.md`:

- `apps/common` — shared utilities
- `apps/website` — Home, About, Functions, FAQ, Careers, Reviews
- `apps/menu` — menu categories, items, pricing
- `apps/gallery` — image gallery
- `apps/promotions` — specials/offers
- `apps/booking` — OpenTable integration
- `apps/contact` — contact form, email, opening hours
- `apps/dashboard` — owner/staff content management

Future-phase apps (`staff`, `roster`, `payroll`, `reports`, `api`, etc.) will
be added under `apps/` when those phases begin.
