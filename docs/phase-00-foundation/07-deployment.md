# Phase 0 – Foundation

# 07 – Deployment Guide

**Project:** Mitch & Antler Platform
**Version:** 1.0
**Status:** Approved Deployment Standard

---

# 1. Purpose

This document defines the deployment strategy for the Mitch & Antler Platform.

The objective is to ensure that every environment—from local development to production—follows a consistent, repeatable, and secure deployment process.

Deployment should require minimal manual intervention and should support future growth.

---

# 2. Deployment Philosophy

The platform should follow these principles:

* Build once, deploy many.
* Development and production should be as similar as practical.
* Configuration belongs outside the application.
* Deployments should be repeatable.
* Rollbacks should be possible.
* Downtime should be minimised.

---

# 3. Environment Overview

The platform uses three environments.

```text
Developer Computer
        │
        ▼
Development Environment
        │
        ▼
Staging Environment (optional)
        │
        ▼
Production Environment
```

Each environment has its own configuration.

---

# 4. Development Environment

Purpose:

Daily software development.

Typical components:

* Python
* Django
* PostgreSQL
* Visual Studio Code
* Git
* Tailwind CSS
* Node.js (build tools only)

Characteristics:

* Debug mode enabled.
* Local database.
* Sample development data.
* Verbose logging.

Production secrets must never be used in development.

---

# 5. Staging Environment

Purpose:

Final testing before production.

Characteristics:

* Mirrors production as closely as possible.
* Uses production-like configuration.
* Connected to a staging database.
* HTTPS enabled.
* Debug mode disabled.

Recommended but optional during early development.

---

# 6. Production Environment

Purpose:

Serve live users.

Characteristics:

* HTTPS only.
* Debug mode disabled.
* Optimised performance.
* Secure environment variables.
* Automated backups.
* Monitoring enabled.

Production must prioritise reliability and security.

---

# 7. Hosting Architecture

Recommended architecture:

```text
Visitors
    │
    ▼
Cloudflare
    │
    ▼
Crazy Domains (DNS)
    │
    ▼
Linux VPS
    │
    ▼
Nginx
    │
    ▼
Gunicorn
    │
    ▼
Django
    │
    ▼
PostgreSQL
```

This architecture is suitable for current requirements and future expansion.

---

# 8. Recommended Server

Recommended operating system:

* Ubuntu LTS

Recommended server size for launch:

* 2 vCPU
* 4 GB RAM
* 40–80 GB SSD

This is sufficient for a café website with an admin dashboard and room to grow.

---

# 9. Domain Configuration

Current domain:

* `mitchandantler.com`

DNS remains managed through Crazy Domains.

Cloudflare is recommended for:

* DNS management
* CDN
* SSL/TLS
* Basic DDoS protection
* Caching

---

# 10. SSL/TLS

Production must use HTTPS.

Cloudflare should provide TLS certificates.

Recommended mode:

* Full (Strict)

All HTTP traffic should redirect to HTTPS.

---

# 11. Web Server

Use Nginx as the reverse proxy.

Responsibilities:

* Serve static files.
* Serve media files (or proxy to object storage).
* Forward requests to Gunicorn.
* Handle HTTPS.
* Compress responses.

---

# 12. Application Server

Gunicorn should serve the Django application.

Responsibilities:

* Run Django.
* Manage worker processes.
* Communicate with Nginx.

Worker count should be tuned based on available CPU and memory.

---

# 13. Database

Production database:

* PostgreSQL

Guidelines:

* Use a dedicated database user.
* Restrict external access.
* Enable regular backups.
* Monitor storage growth.

---

# 14. Static Files

Static assets include:

* CSS
* JavaScript
* Fonts
* Icons
* Logos

Deployment process:

1. Build assets.
2. Run `collectstatic`.
3. Serve through Nginx or WhiteNoise.

---

# 15. Media Files

Media includes:

* Gallery images
* Menu images
* Promotional banners
* Staff profile images

Media should be stored separately from application code.

Future enhancement:

* Object storage (e.g. S3-compatible service).

---

# 16. Environment Variables

Sensitive configuration belongs in environment variables.

Examples:

* Django Secret Key
* Database password
* Resend API key
* Email settings
* Cloudflare credentials

Never hard-code secrets.

---

# 17. Logging

Production logging should include:

* Application log
* Error log
* Security log
* Access log

Logs should rotate automatically to prevent disk exhaustion.

---

# 18. Backups

Automated backups should include:

* PostgreSQL database
* Uploaded media (where practical)
* Configuration files

Backups should be tested by performing periodic restore exercises.

---

# 19. Monitoring

Monitor:

* CPU usage
* Memory usage
* Disk usage
* Database health
* HTTP errors
* Application errors
* SSL certificate status

Monitoring should provide early warning of issues.

---

# 20. Deployment Process

Recommended deployment sequence:

1. Pull latest code.
2. Install/update dependencies.
3. Apply database migrations.
4. Collect static files.
5. Restart application services.
6. Perform smoke tests.
7. Verify logs.
8. Monitor application health.

Every deployment should be repeatable and documented.

---

# 21. Rollback Strategy

If a deployment fails:

1. Stop new deployments.
2. Restore the previous application version.
3. Restore the database only if required.
4. Verify application health.
5. Document the incident.

Rollback procedures should be tested periodically.

---

# 22. Scaling Strategy

As traffic grows, the platform should support:

* Multiple Gunicorn workers.
* Additional application servers.
* Load balancing.
* Database tuning.
* Redis for caching.
* Celery for background tasks.

The application should scale without major architectural changes.

---

# 23. Disaster Recovery

The platform should support recovery from:

* Server failure
* Database corruption
* Accidental deletion
* Configuration errors

Recovery documentation should be maintained and reviewed regularly.

---

# 24. Deployment Checklist

Before every production release:

* All tests pass.
* Database backups completed.
* Environment variables verified.
* Debug mode disabled.
* HTTPS verified.
* Static files collected.
* Migrations reviewed.
* Application starts successfully.
* Smoke tests completed.
* Monitoring operational.

---

# 25. Acceptance Criteria

The deployment strategy is complete when:

* Development, staging, and production environments are defined.
* Hosting architecture is documented.
* Secure deployment practices are established.
* Rollback procedures exist.
* Backup and monitoring strategies are documented.
* Future scaling can occur without redesign.

---

# 26. Related Documents

* 01-overview.md
* 02-architecture.md
* 03-project-structure.md
* 04-development-standards.md
* 05-database-guidelines.md
* 06-security.md
* 08-testing.md
* 09-roadmap.md
* 10-claude-code-prompt.md

---

# Revision History

| Version | Date       | Description                                              |
| ------- | ---------- | -------------------------------------------------------- |
| 1.0     | 2026-07-30 | Initial deployment guide for the Mitch & Antler Platform |
