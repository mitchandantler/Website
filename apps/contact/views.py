from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from apps.common.schema import build_local_business_schema, to_json_ld

from .forms import ContactForm
from .services import send_contact_notification


class ContactView(FormView):
    template_name = "pages/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact:contact")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["restaurant_schema_json"] = to_json_ld(
            build_local_business_schema(self.request)
        )
        return context

    def form_valid(self, form):
        submission = form.save()
        send_contact_notification(submission)
        messages.success(
            self.request, "Thanks for reaching out — we'll be in touch soon."
        )
        return super().form_valid(form)
