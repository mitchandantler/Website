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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from apps.common.sitemaps import StaticViewSitemap
from apps.common.views import robots_txt

sitemaps = {"static": StaticViewSitemap}

urlpatterns = [
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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    if "debug_toolbar" in settings.INSTALLED_APPS:
        urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
