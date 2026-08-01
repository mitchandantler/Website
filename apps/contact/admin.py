from django.contrib import admin

from .models import ContactSubmission, OpeningHours, SpecialHoursOverride


@admin.register(OpeningHours)
class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = ("day_name", "open_time", "close_time", "is_closed")
    list_editable = ("open_time", "close_time", "is_closed")
    ordering = ("day_of_week",)

    def has_add_permission(self, request) -> bool:
        return OpeningHours.objects.count() < 7

    def has_delete_permission(self, request, obj=None) -> bool:
        return False


@admin.register(SpecialHoursOverride)
class SpecialHoursOverrideAdmin(admin.ModelAdmin):
    list_display = ("date", "open_time", "close_time", "is_closed", "note")
    list_filter = ("is_closed",)
    ordering = ("date",)


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "submitted_at", "is_read")
    list_editable = ("is_read",)
    list_filter = ("is_read",)
    search_fields = ("name", "email", "message")
    readonly_fields = ("name", "email", "phone", "message", "submitted_at")

    def has_add_permission(self, request) -> bool:
        return False
