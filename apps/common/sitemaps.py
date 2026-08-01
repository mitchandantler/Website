from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"

    def items(self) -> list[str]:
        return [
            "website:home",
            "website:about",
            "website:reviews",
            "website:faq",
            "menu:menu",
            "gallery:gallery",
            "promotions:offers",
            "booking:booking",
            "booking:order_online",
            "contact:contact",
        ]

    def location(self, item: str) -> str:
        return reverse(item)

    def priority(self, item: str) -> float:
        return 1.0 if item == "website:home" else 0.5
