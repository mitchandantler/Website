# Phase 0 – Foundation

# 10 – AI Development Constitution

**Project:** Mitch & Antler Platform

**Version:** 1.0

**Status:** Mandatory

---

# 1. Purpose

This document defines the permanent development rules for AI coding assistants contributing to the Mitch & Antler Platform.

It applies to every future development task.

The purpose is to ensure that every change made by an AI assistant is:

* Consistent
* Safe
* Modular
* Maintainable
* Production-ready

These rules override any default assumptions made by the AI.

---

# 2. Project Overview

The Mitch & Antler Platform is a modular business platform built using Django and Python.

The long-term vision is to support:

* Public Website
* Owner Dashboard
* Menu Management
* Promotions
* Gallery
* Staff Management
* Payroll
* Roster
* Clock In/Out
* Customer Portal
* Reporting
* Mobile Applications
* Future AI Features

The platform is developed in phases.

---

# 3. Core Principles

Every task must follow these principles:

* Simplicity over complexity.
* Readability over cleverness.
* Maintainability over shortcuts.
* Reuse existing components before creating new ones.
* Respect the documented architecture.

Never introduce unnecessary complexity.

---

# 4. Technology Stack

Backend

* Python
* Django
* Django REST Framework
* PostgreSQL

Frontend

* Django Templates
* HTML5
* Tailwind CSS
* Alpine.js

Preferred libraries should align with the existing architecture.

Do not introduce React, Vue, Angular, or similar frameworks without explicit approval.

---

# 5. Architecture Rules

The AI must:

* Follow the documented folder structure.
* Keep applications modular.
* Keep one responsibility per Django app.
* Reuse shared components.
* Avoid duplicated logic.

Business logic belongs in services, not templates.

---

# 6. Development Workflow

Before implementing a feature:

1. Read the relevant phase documentation.
2. Identify affected modules.
3. Confirm dependencies.
4. Plan the implementation.
5. Implement incrementally.
6. Test the change.
7. Update documentation if required.

Do not skip planning.

---

# 7. Existing Functionality

The AI must preserve existing behaviour unless explicitly instructed otherwise.

Changing unrelated functionality is not permitted.

If a requested change could affect existing features, isolate the implementation to minimise impact.

---

# 8. User Interface Rules

The AI must not redesign the website unless specifically requested.

Preserve:

* Layout
* Colours
* Typography
* Navigation
* Responsive behaviour

New features should integrate with the existing design system.

---

# 9. Coding Standards

The AI must:

* Follow PEP 8.
* Use descriptive names.
* Keep functions small.
* Write readable code.
* Avoid duplication.
* Use type hints where practical.
* Include meaningful docstrings for public classes and functions.

---

# 10. Database Rules

The AI must:

* Use Django models.
* Create migrations for schema changes.
* Use proper relationships.
* Avoid duplicated data.
* Use Decimal fields for currency.
* Include audit fields where appropriate.

Never modify production data directly.

---

# 11. Security Rules

Every feature must:

* Validate user input.
* Respect permissions.
* Protect authenticated pages.
* Use environment variables for secrets.
* Avoid exposing sensitive information.

Security is mandatory.

---

# 12. Documentation Rules

Whenever architecture changes:

* Update the relevant Markdown documents.
* Keep documentation consistent with implementation.
* Add comments only where they explain *why* a decision was made.

Documentation is part of the feature, not an afterthought.

---

# 13. Testing Rules

Before considering a task complete:

* Verify the feature works.
* Confirm existing functionality still works.
* Test edge cases where practical.
* Ensure no obvious regressions.

Critical features should include automated tests.

---

# 14. Third-Party Integrations

Current integrations include:

* OpenTable
* Resend
* In-house QR ordering
* Uber Eats
* DoorDash

Future integrations must follow the same service-based architecture.

Integration logic should remain isolated from core business logic.

---

# 15. Error Handling

Errors should:

* Be handled gracefully.
* Be logged where appropriate.
* Display user-friendly messages.
* Never expose stack traces in production.

---

# 16. Performance Expectations

The AI should:

* Minimise unnecessary database queries.
* Reuse existing data.
* Avoid repeated code.
* Optimise images where appropriate.
* Keep page load times fast.

Optimisation should never sacrifice readability without a measurable benefit.

---

# 17. File Management

The AI should:

* Create new files only when appropriate.
* Reuse existing modules.
* Follow the approved directory structure.
* Avoid duplicate implementations.

Every file should have a clear purpose.

---

# 18. Git Expectations

Changes should be:

* Small
* Focused
* Reversible

Each commit should represent one logical change.

Meaningful commit messages are expected.

---

# 19. Definition of Done

A feature is complete only when:

* Requirements are implemented.
* Code follows project standards.
* Existing functionality remains intact.
* Documentation is updated if necessary.
* Tests pass.
* The feature is production-ready.

---

# 20. Behaviours to Avoid

The AI must not:

* Change unrelated code.
* Introduce unnecessary frameworks.
* Duplicate existing functionality.
* Hard-code secrets.
* Ignore documentation.
* Remove comments without reason.
* Rename files unnecessarily.
* Break backward compatibility without approval.

---

# 21. Preferred Development Order

When implementing new functionality:

1. Models
2. Services
3. Forms
4. Views
5. URLs
6. Templates
7. Admin
8. Tests
9. Documentation

This order encourages a stable and testable implementation.

---

# 22. Long-Term Vision

Every change should contribute to a platform that can support:

* Multiple business modules.
* Future mobile applications.
* AI-assisted features.
* Additional locations.
* Increased customer traffic.
* Future integrations.

The architecture should remain clean and modular as the platform grows.

---

# 23. AI Success Criteria

An AI implementation is successful when:

* It follows this constitution.
* It respects the project architecture.
* It improves the codebase without introducing unnecessary complexity.
* It is understandable to future developers.
* It leaves the project in a better state than before.

---

# 24. Related Documents

* 01-overview.md
* 02-architecture.md
* 03-project-structure.md
* 04-development-standards.md
* 05-database-guidelines.md
* 06-security.md
* 07-deployment.md
* 08-testing.md
* 09-roadmap.md

---

# Revision History

| Version | Date       | Description                                                         |
| ------- | ---------- | ------------------------------------------------------------------- |
| 1.0     | 2026-07-30 | Initial AI Development Constitution for the Mitch & Antler Platform |
