from django.contrib import admin

from order.models import Order


class ItemInline(admin.StackedInline):
    model = Order.items.through
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    """Add items to Order in Admin"""
    inlines = [ItemInline]
    list_filter = ('status',)
    search_fields = ('pk',)
    list_display = ('__str__', 'user', 'total', 'status')
    exclude = ('items',)


admin.site.register(Order, OrderAdmin)
