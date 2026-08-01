from django.contrib import admin
from django.utils.html import format_html

from .models import Promotion


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = (
        "thumbnail",
        "title",
        "start_date",
        "end_date",
        "is_active",
        "display_order",
        "currently_active",
    )
    list_display_links = ("title",)
    list_editable = ("is_active", "display_order")
    list_filter = ("is_active",)
    search_fields = ("title", "description")

    @admin.display(description="Image")
    def thumbnail(self, obj: Promotion) -> str:
        if obj.image:
            return format_html(
                '<img src="{}" style="height:40px;width:40px;'
                'object-fit:cover;border-radius:4px;" />',
                obj.image.url,
            )
        return "—"

    @admin.display(description="Live on Website", boolean=True)
    def currently_active(self, obj: Promotion) -> bool:
        return obj.is_currently_active
