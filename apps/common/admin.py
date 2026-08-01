from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import SiteSetting, Socials


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    # Duplicates the Save buttons at the top of the page (in addition to the
    # bottom) — this is a long form with several fieldsets, and having to
    # scroll all the way down just to save was reported as confusing.
    save_on_top = True

    fieldsets = (
        ("Contact Details", {
            "fields": ("phone_number", "contact_email", "address"),
        }),
        ("Google Maps", {
            "fields": ("google_maps_embed_url",),
        }),
        ("Booking", {
            "fields": ("opentable_embed_url",),
        }),
        ("Order Online", {
            "fields": ("uber_eats_url", "doordash_url", "qr_ordering_url"),
        }),
    )

    def has_add_permission(self, request) -> bool:
        return not SiteSetting.objects.exists()

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def changelist_view(self, request, extra_context=None) -> HttpResponseRedirect:
        obj = SiteSetting.load()
        url = reverse("admin:common_sitesetting_change", args=[obj.pk])
        return HttpResponseRedirect(url)


@admin.register(Socials)
class SocialsAdmin(admin.ModelAdmin):
    fields = ("instagram_url", "facebook_url", "tiktok_url")

    def has_add_permission(self, request) -> bool:
        return not Socials.objects.exists()

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def changelist_view(self, request, extra_context=None) -> HttpResponseRedirect:
        obj = Socials.load()
        url = reverse("admin:common_socials_change", args=[obj.pk])
        return HttpResponseRedirect(url)
