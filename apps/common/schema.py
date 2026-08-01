"""Helpers for embedding schema.org JSON-LD structured data in templates."""

import json

from .models import SiteSetting


def build_local_business_schema(request) -> dict:
    """Base Restaurant/LocalBusiness schema.org dict from SiteSetting.

    Callers (Home, Contact) may add extra keys — e.g. aggregateRating —
    before passing the result to to_json_ld().
    """
    site_settings = SiteSetting.load()
    data = {
        "@context": "https://schema.org",
        "@type": "Restaurant",
        "name": "Mitch & Antler",
        "url": request.build_absolute_uri("/"),
    }
    if site_settings.phone_number:
        data["telephone"] = site_settings.phone_number
    if site_settings.contact_email:
        data["email"] = site_settings.contact_email
    if site_settings.address:
        data["address"] = site_settings.address
    return data


def to_json_ld(data: dict) -> str:
    """Serialize a dict to a JSON-LD string safe to embed in a <script> tag.

    Escapes "</" so the JSON can't prematurely close the surrounding
    <script> element; render with the `safe` filter since this is already
    correctly escaped for its context, not for HTML.
    """
    return json.dumps(data).replace("</", "<\\/")
