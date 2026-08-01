from django.db import models


class SiteSetting(models.Model):
    """Singleton site-wide configuration, shared across every app.

    Always saves to and loads from a single row (pk=1) — see save()/load()
    below — per the admin singleton pattern required in
    docs/phase-01-website/06-admin-dashboard-requirements.md.
    """

    phone_number = models.CharField(max_length=30, blank=True)
    contact_email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    google_maps_embed_url = models.URLField(
        blank=True,
        max_length=350,
        help_text=(
            "Must be a real Google Maps EMBED url, not a share link — a "
            "normal maps.app.goo.gl/google.com/maps/place link will show "
            "'refused to connect' when embedded. To get the right one: open "
            "Google Maps, search this address, click Share > Embed a map, "
            "then copy just the URL from inside the generated "
            "<iframe src=\"...\"> code (it will contain /maps/embed). This "
            "same link is also used for the 'View on Google Maps' link."
        ),
    )
    opentable_embed_url = models.URLField(blank=True, max_length=350)
    uber_eats_url = models.URLField(blank=True, max_length=350)
    doordash_url = models.URLField(blank=True, max_length=350)
    qr_ordering_url = models.URLField(blank=True, max_length=350)
    gift_vouchers_url = models.URLField(blank=True, max_length=350)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def __str__(self) -> str:
        return "Site Settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls) -> "SiteSetting":
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def google_maps_iframe_src(self) -> str:
        """The stored URL, but only if it's actually embeddable.

        Google returns "refused to connect" (X-Frame-Options: SAMEORIGIN)
        when framing a normal maps.app.goo.gl/google.com/maps/place link —
        only a URL from Google's own "Share > Embed a map" dialog (always
        contains "/maps/embed") can actually be framed. If the stored URL
        isn't that format, skip the iframe rather than show a broken one;
        the "View on Google Maps" link still works with any URL type.
        """
        if "/maps/embed" in self.google_maps_embed_url:
            return self.google_maps_embed_url
        return ""


class Socials(models.Model):
    """Singleton social media links — same pattern as SiteSetting, but
    kept as its own admin entry (rather than a fieldset inside Site
    Settings) so it's a clearly separate, easy-to-find section."""

    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    tiktok_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Socials"
        verbose_name_plural = "Socials"

    def __str__(self) -> str:
        return "Socials"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls) -> "Socials":
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
