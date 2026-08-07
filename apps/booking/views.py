from django.views.generic import TemplateView

from apps.common.models import OrderOnline


class BookingView(TemplateView):
    template_name = "pages/booking.html"


class OrderOnlineView(TemplateView):
    template_name = "pages/order_online.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_online = OrderOnline.load()
        options = [
            ("pickup", "Order for Pickup", order_online.qr_ordering_url),
            ("ubereats", "Uber Eats", order_online.uber_eats_url),
            ("doordash", "DoorDash", order_online.doordash_url),
            ("giftvouchers", "Gift Vouchers", order_online.gift_vouchers_url),
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
