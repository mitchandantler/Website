from .models import OrderOnline, SiteSetting, Socials


def site_settings(request):
    """Makes SiteSetting available as `site_settings` in every template."""
    return {"site_settings": SiteSetting.load()}


def socials(request):
    """Makes Socials available as `socials` in every template."""
    return {"socials": Socials.load()}


def order_online(request):
    """Makes OrderOnline available as `order_online` in every template."""
    return {"order_online": OrderOnline.load()}


def canonical_url(request):
    """Absolute URL of the current page, without query string, for
    <link rel="canonical"> and Open Graph og:url."""
    return {"canonical_url": request.build_absolute_uri(request.path)}
