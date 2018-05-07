from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    name_en = models.CharField(max_length=255, verbose_name='Name on English')
    name_de = models.CharField(max_length=255, verbose_name='Name on German')
    description_en = models.TextField(verbose_name='Description on English')
    description_de = models.TextField(verbose_name='Description on German')

    def __str__(self):
        return self.name_en


class Item(models.Model):
    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

    STATUS_CHOICES = (
        (0, 'Not Published'),
        (1, 'Published'),
        (2, 'Sold'),
    )
    sku = models.CharField(max_length=255, verbose_name='SKU')
    title_en = models.CharField(max_length=255, verbose_name='Name on English')
    title_de = models.CharField(max_length=255, verbose_name='Name on German')
    description_en = models.TextField(verbose_name='Description on English')
    description_de = models.TextField(verbose_name='Description on German')
    price = models.IntegerField(verbose_name='Price')
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    author = models.CharField(max_length=255, verbose_name='Author name')
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_en


class ItemPhoto(models.Model):
    item = models.ForeignKey(Item, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item-photos')


class Comment(models.Model):
    item = models.ForeignKey(Item, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comments', on_delete=False)
    body = models.TextField(verbose_name='Comment text')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body
