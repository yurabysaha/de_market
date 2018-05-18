from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from order.models import Order


class ItemInline(admin.TabularInline):
    model = Order.items.through
    extra = 0
    model._meta.verbose_name_plural = _("Order Items")


class OrderAdmin(admin.ModelAdmin):
    """Add items to Order in Admin"""
    inlines = [ItemInline]
    list_filter = ('status',)
    search_fields = ('pk',)
    list_display = ('__str__', 'user', 'total', 'status',)
    exclude = ('items',)


admin.site.register(Order, OrderAdmin)
