from django.contrib import admin, messages
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.html import format_html

from .forms import MenuImportForm
from .models import DietaryTag, MenuCategory, MenuItem
from .services import import_menu_csv


@admin.register(DietaryTag)
class DietaryTagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 0
    fields = ("name", "price", "is_available", "display_order")
    show_change_link = True


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "menu_type", "display_order", "is_active")
    list_filter = ("menu_type", "is_active")
    list_editable = ("display_order", "is_active")
    search_fields = ("name",)
    inlines = [MenuItemInline]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        "thumbnail",
        "name",
        "category",
        "price",
        "is_approved",
        "is_available",
        "display_order",
    )
    list_filter = (
        "is_approved",
        "category__menu_type",
        "category",
        "is_available",
        "dietary_tags",
    )
    list_editable = ("price", "is_approved", "is_available", "display_order")
    search_fields = ("name", "description")
    filter_horizontal = ("dietary_tags",)
    autocomplete_fields = ("category",)
    change_list_template = "admin/menu/menuitem_changelist.html"
    actions = ["approve_selected"]

    @admin.display(description="Image")
    def thumbnail(self, obj: MenuItem) -> str:
        if obj.image:
            return format_html(
                '<img src="{}" style="height:40px;width:40px;'
                'object-fit:cover;border-radius:4px;" />',
                obj.image.url,
            )
        return "—"

    @admin.action(description="Approve selected menu items (show on website)")
    def approve_selected(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(
            request, f"{updated} menu item(s) approved and now live on the website."
        )

    def get_urls(self):
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.import_csv_view),
                name="menu_menuitem_import_csv",
            ),
        ]
        return custom_urls + super().get_urls()

    def import_csv_view(self, request):
        if request.method == "POST":
            form = MenuImportForm(request.POST, request.FILES)
            if form.is_valid():
                result = import_menu_csv(form.cleaned_data["csv_file"])
                for error in result.errors:
                    messages.error(request, error)
                if result.created or result.updated:
                    messages.success(
                        request,
                        f"Menu import complete: {result.created} item(s) "
                        f"created, {result.updated} updated. All imported "
                        "items are unapproved and hidden from the website "
                        "until reviewed — filter by 'Is approved: No' below, "
                        "check each one (including dietary tags), then use "
                        "the 'Approve selected' action to publish them.",
                    )
                elif not result.errors:
                    messages.warning(request, "No rows found to import.")
                return redirect("admin:menu_menuitem_changelist")
        else:
            form = MenuImportForm()

        context = {
            **self.admin_site.each_context(request),
            "title": "Import Menu Items from CSV",
            "form": form,
            "opts": self.model._meta,
        }
        return TemplateResponse(
            request, "admin/menu/import_csv.html", context
        )
