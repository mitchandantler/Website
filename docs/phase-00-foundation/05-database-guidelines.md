# Phase 0 – Foundation

# 05 – Database Guidelines

**Project:** Mitch & Antler Platform
**Version:** 1.0
**Status:** Approved Database Standard

---

# 1. Purpose

This document defines the database architecture, design principles, naming conventions, and data standards for the Mitch & Antler Platform.

The goal is to create a database that is:

* Scalable
* Reliable
* Maintainable
* Secure
* Consistent
* Easy to extend

This document applies to every future Django application.

---

# 2. Database Platform

The platform will use:

**Database Engine**

* PostgreSQL

Reasons:

* Excellent Django support
* ACID compliant
* Reliable
* Highly scalable
* Excellent indexing
* Strong community support

SQLite is only permitted during local development if required.

Production must always use PostgreSQL.

---

# 3. Database Philosophy

The database is the **single source of truth**.

Business rules should never rely on duplicated data.

Design principles:

* Normalize data where practical
* Avoid duplicate information
* Use foreign keys
* Keep tables focused
* Prefer explicit relationships
* Design for future growth

---

# 4. General Naming Standards

## Tables

Use singular model names in Django.

Examples:

```text
MenuItem
MenuCategory
Promotion
GalleryImage
StaffMember
RosterShift
```

Django will create the underlying table names automatically unless explicitly configured.

---

## Fields

Use lowercase with underscores.

Examples:

```text
first_name

last_name

display_order

created_at

updated_at
```

Avoid abbreviations unless universally understood.

---

# 5. Primary Keys

Every model should use:

```python
id
```

provided by Django.

Avoid custom primary keys unless there is a documented business requirement.

---

# 6. Audit Fields

Every major model should include:

```python
created_at

updated_at
```

Optional fields where appropriate:

```python
created_by

updated_by

deleted_at

deleted_by
```

These fields support auditing and troubleshooting.

---

# 7. Status Fields

Where appropriate, include:

```python
is_active
```

For content that can be published or hidden:

```python
is_published
```

Avoid deleting records unnecessarily.

---

# 8. Display Order

Content displayed on the website should include:

```python
display_order
```

Examples:

* Homepage banners
* Menu categories
* Promotions
* Gallery images

This allows business users to reorder content without code changes.

---

# 9. Slugs

Public-facing pages should use:

```python
slug
```

Example:

```text
menu/breakfast

menu/burgers

promotion/winter-special
```

Slugs must be unique where required.

---

# 10. Relationships

Always use proper relationships.

Examples:

```text
MenuCategory

↓

MenuItem
```

```text
Promotion

↓

PromotionImage
```

```text
StaffMember

↓

RosterShift
```

Avoid storing IDs manually as plain text.

---

# 11. Soft Deletion

Where historical data matters, use soft deletion rather than permanently removing records.

Example fields:

```python
deleted_at

deleted_by
```

This is especially important for:

* Staff
* Payroll
* Roster
* Reports

---

# 12. Image Management

Images should never be stored in the database.

The database stores only metadata.

Example:

```text
title

image_path

alt_text

uploaded_at
```

Actual files are stored in the media directory or future object storage.

---

# 13. Menu Design

Menu data should be normalized.

Example:

```text
Category

↓

Menu Item

↓

Menu Image

↓

Dietary Labels
```

Avoid embedding category names repeatedly in multiple tables.

---

# 14. User Model

Use Django's authentication system as the foundation.

Future roles include:

* Super Administrator
* Owner
* Manager
* Supervisor
* Staff
* Customer

Role management should be permission-based rather than duplicated user tables.

---

# 15. Time Standards

Store all timestamps consistently.

Use timezone-aware datetimes.

Display dates according to the application's configured timezone.

---

# 16. Currency Standards

Store money using fixed-precision decimal fields.

Never use floating-point types for prices.

Examples:

* Menu prices
* Payroll
* Sales
* Reports

---

# 17. Boolean Fields

Use booleans only for true/false states.

Examples:

```text
is_active

is_featured

is_published
```

Avoid using booleans where multiple states are expected.

---

# 18. Enumerations

For limited predefined choices, use Django choices or enumerations.

Examples:

* Promotion type
* Staff role
* Booking status
* Shift status

This improves consistency and validation.

---

# 19. Indexing

Create indexes for frequently queried fields.

Examples:

* slug
* email
* created_at
* booking_date
* staff_id

Indexes should be added only where they provide measurable benefit.

---

# 20. Constraints

Use database constraints where appropriate.

Examples:

* Unique email addresses
* Unique slugs
* Positive prices
* Valid foreign keys

Business rules should be enforced at both the application and database levels where practical.

---

# 21. Future Growth

The schema should support future modules without redesign.

Planned additions include:

* Payroll
* Roster
* Loyalty
* Gift Cards
* Inventory
* Kitchen Display
* Customer Accounts
* AI Features

Relationships should be designed with extensibility in mind.

---

# 22. Backup Strategy

Database backups should:

* Run automatically.
* Be encrypted where appropriate.
* Be tested periodically.
* Be retained according to business requirements.

Restoration procedures should be documented and verified.

---

# 23. Migration Standards

Every schema change must use Django migrations.

Guidelines:

* One logical change per migration.
* Review migrations before applying.
* Never edit applied migrations in production.
* Keep migration history under version control.

---

# 24. Performance Considerations

Design queries to:

* Minimise joins where practical.
* Avoid N+1 query problems.
* Use `select_related()` and `prefetch_related()` when appropriate.
* Paginate large datasets.
* Optimise indexes based on real usage.

Performance improvements should be measured rather than assumed.

---

# 25. Acceptance Criteria

The database design is considered compliant when:

* Naming conventions are followed.
* Relationships are properly modelled.
* Audit fields are present.
* Money uses decimal fields.
* Timezones are handled consistently.
* Migrations are used for all schema changes.
* The schema supports future expansion without redesign.

---

# 26. Related Documents

* 01-overview.md
* 02-architecture.md
* 03-project-structure.md
* 04-development-standards.md
* 06-security.md
* 07-deployment.md
* 08-testing.md
* 09-roadmap.md
* 10-claude-code-prompt.md

---

# Revision History

| Version | Date       | Description                                                 |
| ------- | ---------- | ----------------------------------------------------------- |
| 1.0     | 2026-07-30 | Initial database guidelines for the Mitch & Antler Platform |
