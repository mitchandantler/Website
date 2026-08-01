# Phase 0 – Foundation

# 06 – Security Standards

**Project:** Mitch & Antler Platform
**Version:** 1.0
**Status:** Approved

---

# 1. Purpose

This document defines the security standards for the Mitch & Antler Platform.

Security is not a feature that is added later—it is part of every module from the beginning.

These standards apply to:

* Public website
* Admin dashboard
* Staff management
* Payroll
* Roster
* Customer portal
* Mobile APIs
* Third-party integrations

---

# 2. Security Objectives

The platform must:

* Protect customer information.
* Protect staff information.
* Protect payroll data.
* Prevent unauthorized access.
* Secure all communications.
* Reduce the impact of security incidents.
* Support future security enhancements.

---

# 3. Security Principles

The platform follows these principles:

* Secure by default
* Least privilege
* Defence in depth
* Fail securely
* Validate all input
* Escape all output
* Never trust client-side data
* Keep dependencies updated

---

# 4. Authentication

The platform uses Django Authentication.

Authentication responsibilities include:

* Login
* Logout
* Password reset
* Password hashing
* Session management

Passwords are never stored in plain text.

---

# 5. Authorization

Authentication identifies a user.

Authorization determines what they can do.

Permissions should be assigned to roles instead of individual users whenever practical.

Planned roles:

* Super Administrator
* Owner
* Manager
* Supervisor
* Staff
* Customer (Future)

---

# 6. Password Policy

Passwords should:

* Meet minimum length requirements.
* Avoid common passwords.
* Be stored using Django's built-in hashing.
* Never be emailed in plain text.
* Never be visible in logs.

Future enhancement:

* Multi-factor authentication (MFA) for administrators.

---

# 7. Session Management

Sessions should:

* Expire after inactivity.
* Use secure cookies in production.
* Use HTTPOnly cookies.
* Use the Secure flag when HTTPS is enabled.
* Regenerate session identifiers after login.

---

# 8. HTTPS

Production environments must use HTTPS.

All sensitive traffic should be encrypted.

Cloudflare will terminate TLS and forward requests securely to the application server.

---

# 9. Environment Variables

Sensitive information must never be stored in source code.

Store secrets in `.env` files.

Examples:

* Django Secret Key
* Database credentials
* Resend API key
* Cloudflare credentials
* Future payment gateway credentials

The `.env` file must never be committed to Git.

---

# 10. Input Validation

Every user input must be validated on the server.

Examples:

* Contact forms
* Admin forms
* Staff forms
* Payroll data
* Booking requests

Client-side validation improves usability but does not replace server-side validation.

---

# 11. Output Escaping

Templates should rely on Django's automatic escaping.

Do not disable escaping unless there is a documented reason.

Any rich HTML entered through the admin interface should be sanitised before display.

---

# 12. CSRF Protection

Cross-Site Request Forgery (CSRF) protection must remain enabled for all forms and authenticated actions.

Do not disable CSRF globally.

API endpoints should use appropriate authentication mechanisms instead of disabling protection.

---

# 13. File Upload Security

Uploaded files should be validated.

Checks should include:

* File type
* File size
* Allowed extensions

Executable files must never be accepted.

Images should be processed before use where appropriate.

---

# 14. Database Security

Access to the database should be restricted to the application and authorised administrators.

Guidelines:

* Use strong credentials.
* Restrict network access.
* Encrypt backups where practical.
* Apply database updates regularly.

---

# 15. Logging and Auditing

Record important security events such as:

* Login attempts
* Failed logins
* Password resets
* Permission changes
* Administrative actions

Do not log passwords, API keys, or other sensitive secrets.

---

# 16. Error Handling

Users should receive clear, friendly error messages.

Example:

> "Something went wrong. Please try again."

Internal details, stack traces, and configuration information must never be exposed to users.

Detailed errors should be written to application logs.

---

# 17. Third-Party Integrations

All external services should be isolated in dedicated service classes.

Initial integrations include:

* OpenTable
* Resend
* In-house QR ordering
* Uber Eats
* DoorDash

Future integrations should follow the same pattern.

API keys should be stored securely in environment variables.

---

# 18. Admin Dashboard Security

The admin dashboard should:

* Require authentication.
* Enforce role-based permissions.
* Log significant changes.
* Protect against CSRF.
* Validate all submitted data.

Only authorised users should access administrative features.

---

# 19. API Security

Future APIs should:

* Require authentication where appropriate.
* Validate all incoming data.
* Return only necessary information.
* Limit access based on user permissions.
* Be designed with versioning in mind.

Public APIs should expose only the minimum required functionality.

---

# 20. Dependency Management

Dependencies should be:

* Reviewed before addition.
* Kept up to date.
* Removed when no longer needed.

Avoid introducing unnecessary packages.

Prefer mature, well-maintained libraries.

---

# 21. Backup and Recovery

The platform should support:

* Automated database backups.
* Secure backup storage.
* Periodic restore testing.

Recovery procedures should be documented and reviewed regularly.

---

# 22. Incident Response

If a security issue is identified:

1. Contain the issue.
2. Assess the impact.
3. Apply a fix.
4. Verify the resolution.
5. Document the incident.
6. Review lessons learned.

The goal is continuous improvement rather than assigning blame.

---

# 23. Future Enhancements

Planned improvements include:

* Multi-factor authentication (MFA)
* Security headers review
* Automated vulnerability scanning
* Web Application Firewall (WAF) tuning
* Advanced audit reporting
* API rate limiting
* Single Sign-On (SSO) if business needs evolve

---

# 24. Security Checklist

Before deployment, verify:

* HTTPS enabled.
* Environment variables configured.
* Debug mode disabled.
* Strong passwords enforced.
* Admin access restricted.
* Database credentials secured.
* Backups configured.
* Logging enabled.
* File upload validation tested.

---

# 25. Acceptance Criteria

The platform meets the Phase 0 security standard when:

* Authentication and authorization are correctly implemented.
* Secrets are stored securely.
* HTTPS is used in production.
* Server-side validation is in place.
* Administrative actions are auditable.
* Third-party integrations follow secure practices.
* Backup and recovery processes are documented.

---

# 26. Related Documents

* 01-overview.md
* 02-architecture.md
* 03-project-structure.md
* 04-development-standards.md
* 05-database-guidelines.md
* 07-deployment.md
* 08-testing.md
* 09-roadmap.md
* 10-claude-code-prompt.md

---

# Revision History

| Version | Date       | Description                                                |
| ------- | ---------- | ---------------------------------------------------------- |
| 1.0     | 2026-07-30 | Initial security standards for the Mitch & Antler Platform |
