from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models import F
from django.utils.translation import gettext_lazy as _, get_language
from ckeditor.fields import RichTextField


class CategoryManager(models.Manager):

    def get_queryset(self):
        locale = get_language()
        return super().get_queryset().annotate(name=F('name_' + locale),
                                               title=F('seo_' + locale),
                                               seo_desc=F('seo_desc_' + locale),
                                               artist_desc=F('artist_desc_' + locale))


class ItemManager(models.Manager):

    def get_queryset(self):
        locale = get_language()
        return super().get_queryset().annotate(title=F('title_' + str(locale)), description=F('description_' + str(locale)))


class PainterManager(models.Manager):

    def get_queryset(self):
        locale = get_language()
        return super().get_queryset().annotate(photo=F('photo_' + locale))


class Category(models.Model):
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    name_en = models.CharField(max_length=255, verbose_name=_('Name on English'))
    name_de = models.CharField(max_length=255, verbose_name=_('Name on German'))
    artist_photo = models.ImageField(upload_to='artist-photos', verbose_name=_('Painters photo'), null=True, blank=True)
    artist_desc_en = models.TextField(null=True, blank=True, verbose_name=_('Description for Artist on English'))
    artist_desc_de = models.TextField(null=True, blank=True, verbose_name=_('Description for Artist on German'))
    seo_en = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Title for SEO on English'))
    seo_de = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Title for SEO on German'))
    seo_desc_en = models.TextField(null=True, blank=True, verbose_name=_('Description for SEO on English'))
    seo_desc_de = models.TextField(null=True, blank=True, verbose_name=_('Description for SEO on German'))
    parent = models.ForeignKey("Category", null=True, blank=True, on_delete=models.CASCADE, related_name='sub_category', verbose_name=_('Parent Category'))
    updated_at = models.DateTimeField(auto_now=True)

    objects = CategoryManager()

    def __str__(self):
        if not hasattr(self, 'name'):
            locale = get_language()
            return eval('self.name_' + locale)
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('category_detail', args=[str(self.id)])


class Painter(models.Model):
    class Meta:
        verbose_name = _("Painter")
        verbose_name_plural = _("Painters")

    name = models.CharField(max_length=255, verbose_name=_('Painter name'))
    photo_en = models.ImageField(upload_to='painter-photos', verbose_name=_('Picture on English'), null=True)
    photo_de = models.ImageField(upload_to='painter-photos', verbose_name=_('Picture on German'), null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PainterManager()

    def __str__(self):
        return self.name


class Item(models.Model):
    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")
        ordering = ['-created_at']

    STATUS_CHOICES = (
        (0, _('Not Published')),
        (1, _('Published')),
        (2, _('Sold')),
    )
    sku = models.CharField(max_length=255, verbose_name=_('SKU'))
    title_en = models.CharField(max_length=255, verbose_name=_('Name on English'))
    title_de = models.CharField(max_length=255, verbose_name=_('Name on German'))
    description_en = RichTextField(verbose_name=_('Description on English'))
    description_de = RichTextField(verbose_name=_('Description on German'))
    size = models.CharField(max_length=255, verbose_name=_('Size'), blank=True)
    price = models.IntegerField(verbose_name=_('Price'))
    sale_price = models.IntegerField(verbose_name=_('Sale Price'), null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    author = models.ForeignKey(Painter, verbose_name=_('Author'), on_delete=False, null=True, blank=True)
    category = models.ManyToManyField(Category, related_name='items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ItemManager()

    def __str__(self):
        if not hasattr(self, 'title'):
            return self.title_en
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('item-detail', args=[str(self.id)])


class ItemPhoto(models.Model):
    item = models.ForeignKey(Item, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item-photos')
