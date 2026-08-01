# Phase 0 – Foundation

# 02 – System Architecture

**Project:** Mitch & Antler Platform

**Version:** 1.0

**Status:** Approved Architecture

---

# 1. Purpose

This document defines the overall software architecture of the Mitch & Antler Platform.

It serves as the blueprint for every future module and establishes the technical standards that all developers and AI coding assistants must follow.

The architecture is designed to be modular, scalable, secure, and easy to maintain.

---

# 2. Architectural Goals

The platform must:

* Support future business growth without major redesign.
* Keep every business function isolated into reusable Django applications.
* Allow new modules to be added with minimal impact on existing code.
* Provide a consistent user experience across all modules.
* Use a single source of truth for authentication, users, and data.
* Be deployable on a single Django server while remaining cloud-ready.

---

# 3. Architecture Principles

## 3.1 Modular Design

Every business feature must exist as its own Django application.

Examples:

* Website
* Menu
* Promotions
* Gallery
* Staff
* Payroll
* Roster
* Reports

Each application should have one clear responsibility.

---

## 3.2 Loose Coupling

Applications should interact through clearly defined services, models, and APIs rather than relying on direct dependencies wherever possible.

Benefits:

* Easier maintenance
* Independent testing
* Reduced regression risk
* Simpler future expansion

---

## 3.3 High Cohesion

Each application should contain only functionality related to its domain.

For example:

The `menu` app should manage:

* Categories
* Menu Items
* Pricing
* Availability
* Dietary Labels
* Images

It should **not** contain staff management or booking logic.

---

# 4. System Layers

The platform is divided into logical layers.

```text
+----------------------------------------------------+
|                Customer Browser                    |
+----------------------------------------------------+
                     │
                     ▼
+----------------------------------------------------+
|        Django Templates / Tailwind / Alpine        |
+----------------------------------------------------+
                     │
                     ▼
+----------------------------------------------------+
|                 Django Views                       |
+----------------------------------------------------+
                     │
                     ▼
+----------------------------------------------------+
|          Business Logic / Services Layer           |
+----------------------------------------------------+
                     │
                     ▼
+----------------------------------------------------+
|        Django Models / ORM / PostgreSQL            |
+----------------------------------------------------+
```

Every request should flow through these layers.

Business logic should not be placed directly in templates.

---

# 5. High-Level Platform Architecture

```text
                        Internet
                            │
                            ▼
                     Cloudflare CDN
                            │
                            ▼
                     Crazy Domains DNS
                            │
                            ▼
                   Django Application Server
                            │
        ┌─────────────────────────────────────────┐
        │                                         │
        ▼                                         ▼
  Public Website                          Admin Dashboard
        │                                         │
        └───────────────┬─────────────────────────┘
                        ▼
                Business Applications
```

Business applications include:

* Website
* Menu
* Gallery
* Promotions
* Contact
* Booking
* Staff
* Roster
* Payroll
* Reports
* API

All share the same database.

---

# 6. Django Application Structure

Each business domain is implemented as an independent Django app.

Example:

```text
apps/
├── website/
├── menu/
├── gallery/
├── promotions/
├── booking/
├── contact/
├── dashboard/
├── staff/
├── roster/
├── payroll/
├── reports/
├── api/
└── common/
```

The `common` application stores shared utilities, helper functions, reusable components, constants, and services used across multiple apps.

---

# 7. Shared Components

The following components are shared across the platform:

* User authentication
* Roles and permissions
* Navigation
* Layout templates
* Buttons
* Forms
* Notifications
* Email services
* Image processing
* Logging
* Configuration
* Error handling

Shared functionality should not be duplicated.

---

# 8. Authentication Architecture

Authentication will use Django's built-in authentication framework.

The platform will support role-based access control.

Planned roles include:

* Super Administrator
* Owner
* Manager
* Supervisor
* Staff
* Customer (Future)

Permissions must always be assigned to roles rather than directly to users whenever practical.

---

# 9. Database Architecture

The platform uses a single PostgreSQL database.

Advantages:

* Simpler maintenance
* Easier reporting
* Consistent data
* Shared authentication
* Centralized backups

Every Django application stores only the data related to its own domain while sharing common user records where appropriate.

---

# 10. Static and Media Files

The project distinguishes between static assets and uploaded media.

Static assets include:

* CSS
* JavaScript
* Icons
* Fonts
* Logos

Media includes:

* Menu images
* Gallery photos
* Promotional banners
* Staff profile images

Static files are version-controlled.

Media files are user-managed through the admin dashboard.

---

# 11. Admin Dashboard Architecture

The Admin Dashboard is the operational center of the platform.

Its responsibilities include:

* Managing menu items
* Updating promotions
* Uploading gallery images
* Editing opening hours
* Managing staff (future)
* Viewing reports (future)
* Managing content
* Managing site settings

Business users should be able to perform common tasks without modifying code.

---

# 12. Integration Architecture

External services are integrated through dedicated service classes.

Initial integrations include:

* OpenTable (table reservations)
* In-house QR ordering (pickup link)
* Uber Eats
* DoorDash
* Resend (email)

Future integrations may include:

* Google Reviews
* Google Analytics
* Stripe
* Xero
* MYOB

Each integration should be isolated to its own service layer so it can be replaced or updated without affecting other modules.

---

# 13. Scalability Strategy

The architecture is designed to grow over time.

Future modules include:

* Payroll
* Roster
* Clock In/Out
* Loyalty
* Customer Accounts
* Inventory
* Kitchen Display
* AI Assistant
* Mobile API

No existing module should require significant redesign when these are added.

---

# 14. Error Handling

The platform must provide:

* User-friendly error pages
* Structured logging
* Exception handling
* Graceful failure of third-party integrations
* Validation for all user input

Errors should be logged for administrators while displaying clear, non-technical messages to end users.

---

# 15. Security Principles

The platform follows these principles:

* Secure by default
* Least privilege
* Server-side validation
* Encrypted communication (HTTPS)
* Environment variables for secrets
* Audit logging for sensitive actions
* Protection against common web vulnerabilities

Detailed implementation is covered in `06-security.md`.

---

# 16. Deployment Architecture

The initial deployment targets a single production server.

Components:

* Cloudflare
* Crazy Domains (DNS)
* Django
* PostgreSQL
* WhiteNoise for static files

The architecture allows migration to multiple servers or containers in the future without changing application code.

---

# 17. Architectural Decisions

| Decision         | Reason                                                       |
| ---------------- | ------------------------------------------------------------ |
| Django           | Mature, secure, Python-first framework                       |
| PostgreSQL       | Reliable relational database                                 |
| Tailwind CSS     | Fast, consistent UI development                              |
| Alpine.js        | Lightweight interactivity without a heavy frontend framework |
| Django Templates | Excellent SEO and maintainability                            |
| Modular apps     | Easier scaling and maintenance                               |
| Single database  | Simpler operations and reporting                             |
| Service layer    | Clean separation of business logic                           |

---

# 18. Acceptance Criteria

This architecture is considered complete when:

* Every business domain has a defined Django app.
* Shared components are identified.
* External integrations are isolated.
* Security principles are documented.
* Database strategy is defined.
* Deployment approach is documented.
* Future expansion is supported without redesign.

---

# 19. Related Documents

* 01-overview.md
* 03-project-structure.md
* 04-development-standards.md
* 05-database-guidelines.md
* 06-security.md
* 07-deployment.md
* 08-testing.md
* 09-roadmap.md
* 10-claude-code-prompt.md

---

# Revision History

| Version | Date       | Notes                                                       |
| ------- | ---------- | ----------------------------------------------------------- |
| 1.0     | 2026-07-30 | Initial system architecture for the Mitch & Antler Platform |
