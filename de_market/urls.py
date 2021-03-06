"""de_market URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
import debug_toolbar
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap

from de_market.sitemap import ItemSitemap, StaticViewSitemap, CategorySitemap

urlpatterns = []

sitemaps = {
    'item': ItemSitemap,
    'static': StaticViewSitemap,
    'category': CategorySitemap,
}

urlpatterns += i18n_patterns(
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls')),
    path('item/', include('product.urls')),
    path('category/', include('product.category_urls')),
    path('wishlist/', include('wishlist.urls')),
    path('order/', include('order.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
     name='django.contrib.sitemaps.views.sitemap')
)

urlpatterns += [
    url(r'^__debug__/', include(debug_toolbar.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
