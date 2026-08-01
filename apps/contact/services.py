import logging

import resend
from django.conf import settings

from .models import ContactSubmission

logger = logging.getLogger(__name__)


def send_contact_notification(submission: ContactSubmission) -> None:
    """Notify staff of a new contact form submission via Resend.

    Never raises — a failed/unconfigured email must not prevent the
    ContactSubmission from being saved, per
    docs/phase-01-website/07-integrations.md. Failures are logged instead.
    """
    if not settings.RESEND_API_KEY or not settings.CONTACT_NOTIFICATION_EMAIL:
        logger.info(
            "Resend not configured — skipping contact notification email "
            "for submission id=%s.",
            submission.pk,
        )
        return

    resend.api_key = settings.RESEND_API_KEY

    try:
        resend.Emails.send(
            {
                "from": settings.DEFAULT_FROM_EMAIL,
                "to": [settings.CONTACT_NOTIFICATION_EMAIL],
                "reply_to": submission.email,
                "subject": f"New contact form submission from {submission.name}",
                "html": (
                    f"<p><strong>Name:</strong> {submission.name}</p>"
                    f"<p><strong>Email:</strong> {submission.email}</p>"
                    f"<p><strong>Phone:</strong> {submission.phone or '—'}</p>"
                    f"<p><strong>Message:</strong><br>{submission.message}</p>"
                ),
            }
        )
    except Exception:
        logger.exception(
            "Failed to send contact notification email via Resend for "
            "submission id=%s.",
            submission.pk,
        )
