from django.views.generic import TemplateView

from .models import GalleryImage


class GalleryView(TemplateView):
    template_name = "pages/gallery.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["images"] = GalleryImage.objects.filter(is_active=True)
        return context
