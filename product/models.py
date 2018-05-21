from django.contrib.auth.models import User
from django.db import models
from django.db.models import F
from django.utils.translation import gettext_lazy as _, get_language


class CategoryManager(models.Manager):

    def get_queryset(self):
        locale = get_language()
        return super().get_queryset().annotate(name=F('name_' + locale), description=F('description_' + locale))


class ItemManager(models.Manager):

    def get_queryset(self):
        locale = get_language()
        return super().get_queryset().annotate(title=F('title_' + locale), description=F('description_' + locale))


class Category(models.Model):
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    name_en = models.CharField(max_length=255, verbose_name=_('Name on English'))
    name_de = models.CharField(max_length=255, verbose_name=_('Name on German'))
    description_en = models.TextField(verbose_name=_('Description on English'))
    description_de = models.TextField(verbose_name=_('Description on German'))
    parent = models.ForeignKey("Category", null=True, blank=True, on_delete=models.CASCADE, related_name='sub_category', verbose_name=_('Parent Category'))

    objects = CategoryManager()

    def __str__(self):
        if not hasattr(self, 'name'):
            locale = get_language()
            return eval('self.name_' + locale)
        return self.name


class Item(models.Model):
    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")

    STATUS_CHOICES = (
        (0, _('Not Published')),
        (1, _('Published')),
        (2, _('Sold')),
    )
    sku = models.CharField(max_length=255, verbose_name=_('SKU'))
    title_en = models.CharField(max_length=255, verbose_name=_('Name on English'))
    title_de = models.CharField(max_length=255, verbose_name=_('Name on German'))
    description_en = models.TextField(verbose_name=_('Description on English'))
    description_de = models.TextField(verbose_name=_('Description on German'))
    size = models.CharField(max_length=255, verbose_name=_('Size'), blank=True)
    price = models.IntegerField(verbose_name=_('Price'))
    sale_price = models.IntegerField(verbose_name=_('Sale Price'), null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    author = models.CharField(max_length=255, verbose_name=_('Author name'))
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ItemManager()

    def __str__(self):
        if not hasattr(self, 'title'):
            return self.title_en
        return self.title


class ItemPhoto(models.Model):
    item = models.ForeignKey(Item, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item-photos')


class Comment(models.Model):
    item = models.ForeignKey(Item, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comments', on_delete=False)
    body = models.TextField(verbose_name=_('Comment text'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body
