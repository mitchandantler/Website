from django.views.generic import TemplateView

from apps.common.models import SiteSetting


class BookingView(TemplateView):
    template_name = "pages/booking.html"


class OrderOnlineView(TemplateView):
    template_name = "pages/order_online.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site_settings = SiteSetting.load()
        options = [
            ("pickup", "Order for Pickup", site_settings.qr_ordering_url),
            ("ubereats", "Uber Eats", site_settings.uber_eats_url),
            ("doordash", "DoorDash", site_settings.doordash_url),
        ]
        ordering_options = [
            {"key": key, "label": label, "url": url}
            for key, label, url in options
            if url
        ]
        context["ordering_options"] = ordering_options

        # Supports the header nav's hover dropdown linking here with
        # ?method=<key> to pre-select that option in the <select> below.
        requested_key = self.request.GET.get("method")
        selected_option = next(
            (o for o in ordering_options if o["key"] == requested_key), None
        )
        if not selected_option and ordering_options:
            selected_option = ordering_options[0]
        context["initial_selected_url"] = (
            selected_option["url"] if selected_option else ""
        )

        return context
