from django.contrib import admin
from django.utils.html import format_html

from .models import GalleryImage


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("thumbnail", "caption", "alt_text", "display_order", "is_active")
    list_editable = ("display_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("caption", "alt_text")

    @admin.display(description="Preview")
    def thumbnail(self, obj: GalleryImage) -> str:
        if obj.image:
            return format_html(
                '<img src="{}" style="height:48px;width:48px;'
                'object-fit:cover;border-radius:4px;" />',
                obj.image.url,
            )
        return "—"
