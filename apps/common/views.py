from django.http import HttpRequest, HttpResponse
from django.urls import reverse


def robots_txt(request: HttpRequest) -> HttpResponse:
    sitemap_url = request.build_absolute_uri(
        reverse("django.contrib.sitemaps.views.sitemap")
    )
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "",
        f"Sitemap: {sitemap_url}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
