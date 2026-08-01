from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html

from .models import AboutPageContent, FAQItem, HeroImage, HomePageContent, Review


@admin.register(HomePageContent)
class HomePageContentAdmin(admin.ModelAdmin):
    def has_add_permission(self, request) -> bool:
        return not HomePageContent.objects.exists()

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def changelist_view(self, request, extra_context=None) -> HttpResponseRedirect:
        obj = HomePageContent.load()
        url = reverse("admin:website_homepagecontent_change", args=[obj.pk])
        return HttpResponseRedirect(url)


@admin.register(AboutPageContent)
class AboutPageContentAdmin(admin.ModelAdmin):
    def has_add_permission(self, request) -> bool:
        return not AboutPageContent.objects.exists()

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def changelist_view(self, request, extra_context=None) -> HttpResponseRedirect:
        obj = AboutPageContent.load()
        url = reverse("admin:website_aboutpagecontent_change", args=[obj.pk])
        return HttpResponseRedirect(url)


@admin.register(HeroImage)
class HeroImageAdmin(admin.ModelAdmin):
    list_display = ("thumbnail", "alt_text", "display_order", "is_active")
    list_editable = ("display_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("alt_text",)

    @admin.display(description="Preview")
    def thumbnail(self, obj: HeroImage) -> str:
        if obj.image:
            return format_html(
                '<img src="{}" style="height:48px;width:80px;'
                'object-fit:cover;border-radius:4px;" />',
                obj.image.url,
            )
        return "—"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "author_name",
        "rating",
        "source",
        "is_featured",
        "is_active",
        "created_at",
    )
    list_editable = ("is_featured", "is_active")
    list_filter = ("rating", "is_featured", "is_active", "source")
    search_fields = ("author_name", "content")


@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ("question", "display_order", "is_active")
    list_editable = ("display_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("question", "answer")
