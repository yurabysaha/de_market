from django.contrib import admin

from product.models import Item, ItemPhoto, Category


class ItemPhotoInline(admin.TabularInline):
    model = ItemPhoto
    extra = 0


class ItemAdmin(admin.ModelAdmin):
    """Add photos to Item in Admin"""
    inlines = [ItemPhotoInline]
    list_display = ('pk', '__str__', 'status', 'category',)
    list_filter = ('category',)
    search_fields = ('pk',)


admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
