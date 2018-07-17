from django.db.models import Prefetch
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from product.models import Category, Item, ItemPhoto
from product.utils import handle_pagination
from django.utils.translation import gettext as _


def open_detail(request, item_id):
    item = Item.objects.filter(id=item_id).prefetch_related(Prefetch('photos', queryset=ItemPhoto.objects.order_by('id'))).first()
    if not item:
        raise Http404
    items = Item.objects.exclude(id=item_id).exclude(status=0).prefetch_related(Prefetch('photos', queryset=ItemPhoto.objects.order_by('id')))[:3]

    return render(request, 'product/detail.html', {'item': item, 'items': items})


def category_detail(request, category_id):
    cat = get_object_or_404(Category, id=category_id)
    categories = Category.objects.all().prefetch_related('sub_category')

    if cat.sub_category.count() > 0:
        queryset = Item.objects.filter(category__parent=cat)
    else:
        queryset = Item.objects.filter(category__id=category_id)

    items = queryset.prefetch_related(Prefetch('photos', queryset=ItemPhoto.objects.order_by('id')))

    return render(request, 'product/category_detail.html', {'categories': categories,
                                                            'items': handle_pagination(request, items, 12),
                                                            'cat': cat})


def sales_items(request):
    categories = Category.objects.all().prefetch_related('sub_category')
    cat = {'name': _('Discount')}
    items = Item.objects.filter(sale_price__isnull=False).prefetch_related(Prefetch('photos', queryset=ItemPhoto.objects.order_by('id')))

    return render(request, 'product/category_detail.html', {'categories': categories,
                                                            'cat': cat,
                                                            'items': handle_pagination(request, items, 12)})
