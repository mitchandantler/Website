# Phase 1 — Public Website
## Overview

Version: 1.0
Phase Owner: Mitch & Antler
Related Roadmap: `project_phases.md`

---

## Purpose

Deliver the customer-facing public website for Mitch & Antler. This is the first
customer-visible deliverable of the platform and establishes the design language,
content structure, and technical foundation that later phases (Staff Management,
Customer Platform, Business Intelligence) will build on top of.

---

## Scope

In scope for Phase 1:

- Marketing / informational website (Home, About, Menu, Gallery, Contact, FAQ, Careers)
- Menu display (Food + Drink)
- Booking via OpenTable integration
- Online ordering links (Uber Eats, DoorDash, QR ordering)
- Reviews display
- Admin dashboard for managing website content (menu items, promotions, gallery, hours)
- SEO fundamentals

Out of scope for Phase 1 (deferred to later phases):

- Staff-facing features (rostering, payroll, clock in/out) — Phase 2
- Customer accounts, loyalty, gift cards — Phase 3
- Reporting and analytics — Phase 4
- Native mobile apps, KDS, multi-location — Phase 5

---

## Goals

- Fast, mobile-first, SEO-friendly public website
- Content (menu, hours, promotions, gallery) manageable by non-technical staff via
  an admin dashboard — no code changes required for day-to-day content updates
- Clean integration points for third-party services (OpenTable, Uber Eats, DoorDash,
  Google Maps) without tightly coupling the codebase to any one of them
- Foundation reused by later phases (auth, base templates, design system, deployment
  pipeline)

---

## Success Criteria

- Public website live at mitchandantler.com
- All Phase 1 features (see `02-functional-requirements.md`) implemented and tested
- Admin dashboard allows staff to update menu, hours, gallery, and promotions without
  developer involvement
- Lighthouse/PageSpeed scores meet targets defined in `08-seo-requirements.md`
- All pages mobile responsive
- Deployed and monitored per `07-deployment.md` from Phase 0

---

## Related Documents

- `02-functional-requirements.md` — detailed feature requirements
- `03-sitemap-navigation.md` — page structure and navigation
- `04-ui-ux-specification.md` — design and UX guidelines
- `05-database-models.md` — data model for website content
- `06-admin-dashboard-requirements.md` — admin/staff content management
- `07-integrations.md` — third-party integrations
- `08-seo-requirements.md` — SEO and performance targets
- `09-testing-checklist.md` — QA checklist
- `10-claude-code-implementation-prompt.md` — implementation prompt for Claude Code
