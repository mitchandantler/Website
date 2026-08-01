# Phase 1 — Public Website
## Claude Code Implementation Prompt

---

## Purpose

This document is the prompt to give Claude Code (or a similar coding agent)
when beginning implementation of Phase 1. It consolidates the requirements
from the other documents in `docs/phase-01-website/` into a single actionable
brief.

---

## Prompt

```
You are implementing Phase 1 ("Public Website") of the Mitch & Antler
Platform, a modular Django-based business management system for a café.

Read the following documents in docs/phase-01-website/ before writing any
code, and follow them as the source of truth:
- 01-website-overview.md — purpose, scope, goals
- 02-functional-requirements.md — feature list
- 03-sitemap-navigation.md — page structure and navigation
- 04-ui-ux-specification.md — design system and UX guidelines
- 05-database-models.md — data models to implement
- 06-admin-dashboard-requirements.md — admin/content management requirements
- 07-integrations.md — third-party integrations (OpenTable, Uber Eats,
  DoorDash, Google Maps, Resend)
- 08-seo-requirements.md — SEO and performance targets
- 09-testing-checklist.md — QA checklist to satisfy before calling this done

Also read ../project_phases.md for the overall platform vision and tech
stack (Python/Django, Django REST Framework, PostgreSQL, Django Templates,
Tailwind CSS, Alpine.js, HTMX, WhiteNoise, Pillow, Resend, Cloudflare).

Requirements:
1. Build a Django app (e.g. `website`) implementing the models in
   05-database-models.md.
2. Implement all public-facing pages listed in 03-sitemap-navigation.md,
   using Django Templates + Tailwind CSS, mobile-first and responsive.
3. Register all content models in Django Admin per
   06-admin-dashboard-requirements.md, with sensible list_display,
   search_fields, list_filter, and image thumbnail previews. Set up the two
   roles (Owner/Admin, Content Editor) using Django's Group/Permission
   system.
4. Wire up the integrations described in 07-integrations.md. All third-party
   URLs and API keys must be configurable (via SiteSetting model or
   environment variables) — never hardcoded.
5. Implement the Contact form with server-side validation, CSRF protection,
   and Resend email notification on submission. Email failure must not
   prevent the ContactSubmission from being saved; log failures.
6. Apply the SEO requirements in 08-seo-requirements.md: meta tags per page,
   sitemap.xml, robots.txt, structured data (Restaurant/LocalBusiness,
   FAQPage), Open Graph tags, image alt text, lazy loading.
7. Follow the platform coding standards from project_phases.md: modular,
   reusable components, no duplicate code, mobile responsive, production
   ready, documented.
8. Do not implement anything from later phases (staff management, customer
   accounts/loyalty, reporting, native mobile apps) — keep scope to Phase 1
   only.
9. Before considering the work complete, verify it against every item in
   09-testing-checklist.md.

Work incrementally: models + admin first, then templates/pages, then
integrations, then SEO polish, then run through the testing checklist.
Flag any ambiguity (e.g. missing brand colours/logo, missing real
OpenTable/Uber Eats/DoorDash URLs) rather than inventing production values —
use clearly-marked placeholders that are easy to swap.
```

---

## Notes for Whoever Runs This Prompt

- Brand assets (logo, colour palette, fonts) and real third-party URLs/API
  keys should be supplied before final content population — placeholders are
  acceptable for initial development.
- This prompt assumes Phase 0 (Foundation) is already complete — Django
  project setup, auth, base templates/design system, deployment pipeline,
  and environment/security configuration should already exist. If Phase 0 is
  not yet done, do that first (see `../phase-00-foundation/`).
