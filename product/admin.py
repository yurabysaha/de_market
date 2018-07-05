import random

from datetime import datetime
from django.contrib import admin
from django.http import HttpResponseRedirect

from product.models import Item, ItemPhoto, Category, Painter


class ItemPhotoInline(admin.TabularInline):
    model = ItemPhoto
    extra = 0


class ItemAdmin(admin.ModelAdmin):
    """Add photos to Item in Admin"""
    inlines = [ItemPhotoInline]
    list_display = ('sku', '__str__', 'status',)
    list_filter = ('category',)
    search_fields = ('sku',)
    readonly_fields = ('sku',)
    filter_horizontal = ('category',)

    def save_model(self, request, obj, form, change):
        """Add SKU to Item."""
        super().save_model(request, obj, form, change)
        if not obj.sku:
            obj.sku = str(obj.id) + str(random.randint(100, 999))
            obj.save()

    change_form_template = 'admin/product/item/change_form.html'

    def response_change(self, request, obj):
        if "_set_point_for_places" in request.POST:
            obj.created_at = datetime.now()
            obj.save()

            self.message_user(request, "This picture now in top")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
admin.site.register(Painter)
