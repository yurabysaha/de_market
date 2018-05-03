from django.contrib import admin

from product.models import Item, ItemPhoto, Category


class ItemPhotoInline(admin.TabularInline):
    model = ItemPhoto
    extra = 1


class ItemAdmin(admin.ModelAdmin):
    """Add photos to Item in Admin"""
    inlines = [ItemPhotoInline]


admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
