from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from product.models import Item, Category


class ItemSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5
    i18n = True

    def items(self):
        return Item.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class CategorySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5
    i18n = True

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'
    i18n = True

    def items(self):
        return ['home', 'about_us', 'delivery']

    def location(self, item):
        return reverse(item)