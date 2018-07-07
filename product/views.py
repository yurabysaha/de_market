from django.http import Http404
from django.shortcuts import render, get_object_or_404
from product.models import Category, Item
from product.utils import handle_pagination
from django.utils.translation import gettext as _


def open_detail(request, item_id):
    item = Item.objects.filter(id=item_id).first()
    if not item:
        raise Http404
    items = Item.objects.exclude(id=item_id).exclude(status=0)[:3]

    return render(request, 'product/detail.html', {'item': item, 'items': items})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'home.html', {'categories': categories})


def category_detail(request, category_id):
    cat = get_object_or_404(Category, id=category_id)
    categories = Category.objects.all()

    if cat.sub_category.count() > 0:
        items = Item.objects.filter(category__parent=cat)
    else:
        items = Item.objects.filter(category__id=category_id)

    item = Item.objects.filter(category__id=category_id).first()
    sub_categories = cat.sub_category.all()
    return render(request, 'product/category_detail.html', {'categories': categories,
                                                            'items': handle_pagination(request, items, 12),
                                                            'cat': cat,
                                                            'item': item,
                                                            'sub_categories': sub_categories})


def sales_items(request):
    categories = Category.objects.all()
    cat = {'name': _('Discount')}
    items = Item.objects.filter(sale_price__isnull=False)

    return render(request, 'product/category_detail.html', {'categories': categories,
                                                            'cat': cat,
                                                            'items': handle_pagination(request, items, 12)})
