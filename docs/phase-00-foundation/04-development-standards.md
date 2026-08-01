# Phase 0 – Foundation

# 04 – Development Standards

**Project:** Mitch & Antler Platform
**Version:** 1.0
**Status:** Approved Development Standard

---

# 1. Purpose

This document defines the development standards for the Mitch & Antler Platform.

Every developer, AI coding assistant, and contributor must follow these standards.

The objective is to ensure that the entire codebase remains:

* Consistent
* Readable
* Maintainable
* Testable
* Secure
* Scalable

These standards apply to every phase of the project.

---

# 2. Core Development Principles

Every piece of code should be:

* Easy to understand
* Easy to modify
* Easy to test
* Easy to document
* Easy to reuse

When making development decisions, always prefer simplicity over unnecessary complexity.

---

# 3. Technology Standards

## Backend

* Python 3.13+
* Django 5.x
* Django REST Framework
* PostgreSQL

## Frontend

* Django Templates
* HTML5
* Tailwind CSS
* Alpine.js
* HTMX (where appropriate)

Heavy JavaScript frameworks (React, Vue, Angular, etc.) should not be introduced unless there is a clear business requirement and architectural approval.

---

# 4. Python Standards

Follow:

* PEP 8
* PEP 257 (Docstrings)
* Python type hints where practical

Example:

```python
def calculate_price(item_price: float, gst: float) -> float:
    """Calculate the total price including GST."""
    return item_price + gst
```

---

# 5. Django Standards

Use Django conventions whenever possible.

Examples:

* Models belong in `models.py`
* Forms belong in `forms.py`
* Admin configuration belongs in `admin.py`
* URLs belong in `urls.py`
* Signals belong in `signals.py`
* Business logic belongs in `services.py`

Do not bypass Django's built-in features unless there is a documented reason.

---

# 6. Business Logic

Views should remain lightweight.

Business logic should be placed in dedicated service classes or helper functions.

Good example:

```text
menu/
├── services.py
├── models.py
├── views.py
```

Responsibilities of `services.py` may include:

* Price calculations
* Import/export
* Availability checks
* Email preparation
* Third-party integrations

---

# 7. HTML Standards

Templates should:

* Extend `base.html`
* Use reusable partials
* Avoid duplicated markup
* Keep logic minimal

Preferred structure:

```text
templates/
├── base.html
├── components/
├── partials/
├── pages/
└── emails/
```

---

# 8. CSS Standards

Use Tailwind CSS utilities as the primary styling method.

Avoid:

* Inline styles
* Duplicate CSS
* Large custom CSS files

Create reusable components instead of repeating classes.

---

# 9. JavaScript Standards

Use Alpine.js for lightweight interactions.

Examples:

* Mobile navigation
* Dropdown menus
* Accordions
* Image galleries
* Confirmation dialogs

Avoid large custom JavaScript unless necessary.

---

# 10. Database Standards

Every model should include audit fields where appropriate:

```python
created_at
updated_at
```

Consider adding:

* `is_active`
* `display_order`
* `slug`

Avoid duplicated data and enforce relationships with foreign keys.

---

# 11. Naming Conventions

## Classes

Use PascalCase.

Examples:

```text
MenuItem
Promotion
StaffMember
RosterShift
```

## Functions

Use snake_case.

Examples:

```text
calculate_total()

send_notification()

create_shift()
```

## Variables

Use descriptive names.

Good:

```text
menu_item
staff_member
promotion_banner
```

Avoid abbreviations such as:

```text
itm
tmp
obj
x
```

unless they are appropriate in a very small scope.

---

# 12. Comments

Write comments to explain **why**, not **what**.

Bad:

```python
# Increment x
x += 1
```

Good:

```python
# Increase the visit count after a successful booking
visit_count += 1
```

Clear code should reduce the need for comments.

---

# 13. Documentation Standards

Every Django app must include a `README.md` describing:

* Purpose
* Models
* URLs
* Services
* Dependencies
* Future improvements

Complex functions should include meaningful docstrings.

---

# 14. Error Handling

Never silently ignore errors.

Use:

* Logging
* Meaningful exceptions
* User-friendly messages

Do not expose stack traces or sensitive information to end users.

---

# 15. Logging Standards

Log important events such as:

* Failed logins
* Administrative changes
* Import/export operations
* Integration failures

Do not log:

* Passwords
* API keys
* Sensitive personal information

---

# 16. Git Workflow

Recommended branches:

```text
main
develop
feature/<feature-name>
bugfix/<issue>
release/<version>
hotfix/<issue>
```

Guidelines:

* Never commit directly to `main`.
* Keep commits focused on a single change.
* Write clear commit messages.

Example:

```text
Add menu category management

Fix promotion image upload

Implement OpenTable booking integration
```

---

# 17. Testing Standards

Every new feature should be tested before merging.

Testing should include:

* Model validation
* View behaviour
* Forms
* Permissions
* Business logic
* Integrations (where practical)

Critical workflows should have automated tests.

---

# 18. Security Standards

Always:

* Validate server-side input.
* Escape output where appropriate.
* Use Django CSRF protection.
* Protect sensitive views with authentication and permissions.
* Store secrets in environment variables.

Never hard-code credentials.

---

# 19. Performance Standards

Optimise for speed and maintainability.

Guidelines:

* Use database indexes where appropriate.
* Avoid unnecessary database queries.
* Paginate large lists.
* Optimise uploaded images.
* Cache expensive operations if needed.

Performance improvements should not sacrifice readability without justification.

---

# 20. AI Development Standards

When using AI coding assistants:

* Follow existing architecture.
* Do not introduce new frameworks without approval.
* Reuse existing components.
* Preserve current functionality unless instructed otherwise.
* Keep changes focused on the requested feature.
* Update documentation when architecture changes.
* Prefer maintainability over clever solutions.

---

# 21. Code Review Checklist

Before merging any feature, verify:

* Code follows project standards.
* No duplicated logic.
* Naming is consistent.
* Tests pass.
* Documentation is updated.
* No secrets are committed.
* Existing functionality remains intact.

---

# 22. Definition of Done

A feature is considered complete only when:

* Functional requirements are met.
* Code follows these standards.
* Documentation is updated.
* Tests pass.
* No critical defects remain.
* The feature is ready for production deployment.

---

# 23. Acceptance Criteria

This document is successful when:

* All contributors follow a consistent coding style.
* New modules integrate without structural changes.
* AI-generated code aligns with project architecture.
* Maintenance effort is reduced through consistency.
* The project remains understandable to future developers.

---

# 24. Related Documents

* 01-overview.md
* 02-architecture.md
* 03-project-structure.md
* 05-database-guidelines.md
* 06-security.md
* 07-deployment.md
* 08-testing.md
* 09-roadmap.md
* 10-claude-code-prompt.md

---

# Revision History

| Version | Date       | Description                                                   |
| ------- | ---------- | ------------------------------------------------------------- |
| 1.0     | 2026-07-30 | Initial development standards for the Mitch & Antler Platform |
