from django.db.models import Avg
from django.views.generic import TemplateView

from apps.common.schema import build_local_business_schema, to_json_ld
from apps.promotions.models import Promotion

from .models import FAQItem, HeroImage, HomePageContent, Review


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hero_content"] = HomePageContent.load()
        context["hero_images"] = HeroImage.objects.filter(is_active=True)
        context["featured_promotions"] = Promotion.objects.currently_active()[:3]

        reviews = Review.objects.filter(is_active=True)
        context["featured_reviews"] = reviews.filter(is_featured=True)[:3]

        schema = build_local_business_schema(self.request)
        if reviews.exists():
            schema["aggregateRating"] = {
                "@type": "AggregateRating",
                "ratingValue": round(reviews.aggregate(avg=Avg("rating"))["avg"], 1),
                "reviewCount": reviews.count(),
            }
        context["restaurant_schema_json"] = to_json_ld(schema)

        return context


class AboutView(TemplateView):
    template_name = "pages/about.html"


class ReviewsView(TemplateView):
    template_name = "pages/reviews.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = Review.objects.filter(is_active=True)
        return context


class FAQView(TemplateView):
    template_name = "pages/faq.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        faq_items = FAQItem.objects.filter(is_active=True)
        context["faq_items"] = faq_items

        if faq_items:
            data = {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": item.question,
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": item.answer,
                        },
                    }
                    for item in faq_items
                ],
            }
            context["faq_schema_json"] = to_json_ld(data)

        return context
