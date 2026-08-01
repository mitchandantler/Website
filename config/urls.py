"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import re

from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path
from django.views.static import serve as serve_static

from apps.common.sitemaps import StaticViewSitemap
from apps.common.views import robots_txt

sitemaps = {"static": StaticViewSitemap}

urlpatterns = [
    # Must come before admin.site.urls — these give the admin login page's
    # built-in "Forgotten your login credentials?" link (it only appears if
    # a URL named 'admin_password_reset' resolves) a real destination.
    path('admin/password_reset/', auth_views.PasswordResetView.as_view(), name='admin_password_reset'),
    path('admin/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('admin/', admin.site.urls),
    path('robots.txt', robots_txt, name='robots_txt'),
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap',
    ),
    path('menu/', include('apps.menu.urls')),
    path('gallery/', include('apps.gallery.urls')),
    path('offers/', include('apps.promotions.urls')),
    path('contact/', include('apps.contact.urls')),
    path('', include('apps.booking.urls')),
    path('', include('apps.website.urls')),
]

# Registered directly (not via django.conf.urls.static.static(), which has
# its own internal `if not settings.DEBUG: return []` guard — wrapping or
# unwrapping it in our own DEBUG check has no effect, it's still a no-op in
# production either way). Served in every environment because Render has no
# separate web server or S3/R2 storage configured for user-uploaded media
# yet, so without this route /media/* 404s regardless of whether the file
# exists. Fine for this site's traffic level; revisit if that changes.
urlpatterns += [
    re_path(
        r"^%s(?P<path>.*)$" % re.escape(settings.MEDIA_URL.lstrip("/")),
        serve_static,
        {"document_root": settings.MEDIA_ROOT},
    ),
]

if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
