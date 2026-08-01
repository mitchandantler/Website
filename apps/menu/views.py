from django.db.models import Prefetch
from django.views.generic import TemplateView

from apps.common.schema import to_json_ld

from .models import MenuCategory, MenuItem


class MenuView(TemplateView):
    template_name = "pages/menu.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        available_items = Prefetch(
            "items",
            queryset=MenuItem.objects.filter(
                is_available=True, is_approved=True
            ).prefetch_related("dietary_tags"),
        )

        food_categories = MenuCategory.objects.filter(
            menu_type=MenuCategory.MenuType.FOOD, is_active=True
        ).prefetch_related(available_items)

        drink_categories = MenuCategory.objects.filter(
            menu_type=MenuCategory.MenuType.DRINK, is_active=True
        ).prefetch_related(available_items)

        all_categories = list(food_categories) + list(drink_categories)
        categories = [category for category in all_categories if category.items.all()]
        context["categories"] = categories

        menu_sections = [
            {
                "@type": "MenuSection",
                "name": category.name,
                "hasMenuItem": [
                    {
                        "@type": "MenuItem",
                        "name": item.name,
                        "description": item.description,
                        "offers": {
                            "@type": "Offer",
                            "price": str(item.price),
                            "priceCurrency": "AUD",
                        },
                    }
                    for item in category.items.all()
                ],
            }
            for category in categories
        ]

        if menu_sections:
            data = {
                "@context": "https://schema.org",
                "@type": "Menu",
                "hasMenuSection": menu_sections,
            }
            context["menu_schema_json"] = to_json_ld(data)

        return context
