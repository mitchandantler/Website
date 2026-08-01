# Phase 0 – Foundation

# 03 – Project Structure

**Project:** Mitch & Antler Platform

**Version:** 1.0

**Status:** Approved

---

# 1. Purpose

This document defines the standard folder structure, naming conventions, and organization of the Mitch & Antler Platform.

Every developer and AI coding assistant must follow this structure. New features should fit into the existing architecture rather than creating new patterns.

The goals are:

* Consistency
* Scalability
* Readability
* Maintainability
* Reusability

---

# 2. Core Principles

The project structure must follow these rules:

* One responsibility per Django app.
* Keep related code together.
* Avoid duplicate code.
* Separate business logic from presentation.
* Group shared functionality in common libraries.
* Organize documentation alongside development.

---

# 3. Root Directory Structure

```text
mitchandantler/
│
├── apps/
├── config/
├── templates/
├── static/
├── media/
├── docs/
├── tests/
├── requirements/
├── scripts/
├── logs/
├── .env
├── .gitignore
├── manage.py
├── README.md
└── pyproject.toml
```

### Directory Descriptions

| Directory       | Purpose                          |
| --------------- | -------------------------------- |
| `apps/`         | Django applications              |
| `config/`       | Django project configuration     |
| `templates/`    | Shared HTML templates            |
| `static/`       | CSS, JavaScript, fonts, icons    |
| `media/`        | Uploaded files and images        |
| `docs/`         | Project documentation            |
| `tests/`        | Integration and end-to-end tests |
| `requirements/` | Python dependency files          |
| `scripts/`      | Utility scripts                  |
| `logs/`         | Application logs                 |

---

# 4. Django Apps

Every business feature must exist as its own Django application.

```text
apps/

common/
website/
menu/
gallery/
promotions/
booking/
contact/
dashboard/

staff/
roster/
payroll/
clockin/

reports/
analytics/

api/
```

---

# 5. Purpose of Each App

## common

Shared utilities.

Examples:

* helper functions
* reusable services
* validators
* constants
* permissions
* email helpers
* image utilities

---

## website

Customer-facing pages.

* Home
* About
* Contact
* Functions
* FAQ

---

## menu

Responsible only for menu management.

* Categories
* Menu Items
* Pricing
* Availability
* Dietary Labels

---

## gallery

Stores and displays images.

* Gallery albums
* Homepage images
* Promotional images

---

## promotions

Marketing content.

* Specials
* Seasonal campaigns
* Featured items
* Homepage banners

---

## booking

Handles reservation integrations.

Current:

* OpenTable

Future:

* Native booking system

---

## contact

Customer enquiries.

* Contact form
* Email
* Map
* Opening hours

---

## dashboard

Owner management interface.

Examples:

* Dashboard
* Content management
* Settings
* Quick statistics

---

## staff

Employee records.

Future module.

---

## roster

Roster management.

Future module.

---

## payroll

Payroll processing.

Future module.

---

## clockin

Clock In / Clock Out.

Future module.

---

## reports

Business reporting.

Future module.

---

## analytics

Business intelligence.

Future module.

---

## api

REST API.

Used by:

* Mobile App
* Kiosk
* Third-party integrations

---

# 6. Standard Django App Structure

Every application should use the same internal layout.

```text
menu/

admin.py

apps.py

models.py

views.py

urls.py

forms.py

services.py

validators.py

signals.py

permissions.py

tests.py

README.md

templates/

static/

migrations/
```

This consistency makes navigation easier and reduces onboarding time.

---

# 7. Configuration Structure

```text
config/

settings/

base.py

development.py

staging.py

production.py

urls.py

wsgi.py

asgi.py
```

Environment-specific settings should never be mixed together.

---

# 8. Documentation Structure

```text
docs/

phase-00-foundation/

phase-01-website/

phase-02-staff/

phase-03-customer/

phase-04-analytics/

phase-05-future/
```

Each phase contains its own documentation.

---

# 9. Static Assets

```text
static/

css/

js/

images/

icons/

fonts/
```

Rules:

* Organize by type.
* Use descriptive names.
* Minify production assets where practical.

---

# 10. Media Files

```text
media/

menu/

gallery/

promotions/

staff/

uploads/
```

Media should never be committed to Git.

---

# 11. Templates

Shared templates:

```text
templates/

base.html

partials/

components/

pages/

emails/
```

### Components

Reusable pieces such as:

* Navigation
* Footer
* Buttons
* Cards
* Forms
* Alerts
* Modals

Components should be reused instead of duplicated.

---

# 12. Business Logic

Business logic belongs in service classes where appropriate.

Example:

```text
menu/

services.py
```

Responsibilities include:

* Pricing calculations
* Availability checks
* Image processing
* Import/export operations

Views should remain lightweight.

---

# 13. Naming Conventions

## Files

Use lowercase with underscores.

Examples:

* menu_item.py
* email_service.py
* report_generator.py

---

## Classes

Use PascalCase.

Example:

```python
MenuItem
PromotionService
RosterManager
```

---

## Functions

Use snake_case.

Example:

```python
calculate_total()

send_email()

generate_report()
```

---

## Variables

Use descriptive snake_case names.

Good:

```python
menu_item
promotion_banner
staff_member
```

Avoid abbreviations unless they are universally understood.

---

# 14. URL Design

URLs should be clean and predictable.

Examples:

```text
/

about/

menu/

menu/breakfast/

gallery/

promotions/

contact/

dashboard/

staff/
```

Avoid unnecessary nesting.

---

# 15. Reusable Components

Examples include:

* Navigation bar
* Footer
* Hero banner
* Menu card
* Promotion card
* Gallery card
* Buttons
* Breadcrumbs
* Forms

Every component should have one source of truth.

---

# 16. Git Branch Strategy

Suggested branches:

```text
main

develop

feature/menu

feature/gallery

feature/dashboard

bugfix/menu-price

release/v1.0
```

Do not develop directly on `main`.

---

# 17. Dependency Management

Use a dedicated `requirements/` directory.

Suggested files:

```text
requirements/

base.txt

development.txt

production.txt
```

This keeps environments clean and reproducible.

---

# 18. Logging

Application logs should be written to:

```text
logs/

application.log

error.log

security.log
```

Logs should never contain sensitive information such as passwords or API keys.

---

# 19. Environment Variables

Store secrets in the `.env` file.

Examples:

* Secret Key
* Database credentials
* Email API keys
* Cloudflare tokens
* Resend API key

Never commit `.env` to version control.

---

# 20. Acceptance Criteria

The project structure is complete when:

* Every Django app follows the standard layout.
* Shared code resides in `common`.
* Documentation is organized by phase.
* Static and media files are separated.
* Templates are reusable.
* Configuration is environment-specific.
* Naming conventions are consistently applied.

---

# 21. Future Expansion

The structure is designed so that new apps—such as Inventory, Kitchen Display, Loyalty, Supplier Portal, or AI Assistant—can be added under `apps/` without changing the existing organization.

---

# 22. Related Documents

* 01-overview.md
* 02-architecture.md
* 04-development-standards.md
* 05-database-guidelines.md
* 06-security.md
* 07-deployment.md
* 08-testing.md
* 09-roadmap.md
* 10-claude-code-prompt.md

---

# Revision History

| Version | Date       | Description                             |
| ------- | ---------- | --------------------------------------- |
| 1.0     | 2026-07-30 | Initial project structure specification |
