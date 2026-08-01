"""Custom ordering for the Django Admin index page.

By default Django lists apps alphabetically, which buries the
day-to-day content sections (Site Settings, Socials, Menu, etc.) under
"Authentication and Authorization". This reorders the index so the
sections staff actually use daily come first, with Auth pushed to the
bottom since it's rarely touched.
"""

from django.contrib.admin.sites import AdminSite

APP_ORDER = [
    "common",
    "website",
    "menu",
    "gallery",
    "promotions",
    "contact",
    "booking",
    "dashboard",
    "auth",
]


def _ordered_get_app_list(self, request, app_label=None):
    app_dict = self._build_app_dict(request, app_label)

    def sort_key(app):
        try:
            return APP_ORDER.index(app["app_label"])
        except ValueError:
            return len(APP_ORDER)

    return sorted(app_dict.values(), key=sort_key)


AdminSite.get_app_list = _ordered_get_app_list
