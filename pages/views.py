from django.shortcuts import render

from product.models import Category, Item
from product.utils import handle_pagination


def home(request):
    items = Item.objects.exclude(status=0)
    categories = Category.objects.all()
    return render(request, 'home.html', {'items': handle_pagination(request, items, 12), 'categories': categories})


def about_us(request):
    categories = Category.objects.all()
    return render(request, 'about_us.html', {'categories': categories})


def delivery(request):
    categories = Category.objects.all()
    return render(request, 'delivery.html', {'categories': categories})


def faq(request):
    categories = Category.objects.all()
    return render(request, 'faq.html', {'categories': categories})


def search(request):
    categories = Category.objects.all()
    item_name = request.GET.get('q', None)
    category_id = request.GET.get('qcategory', None)
    art = request.GET.get('art', None)
    min_price = request.GET.get('min', None)
    max_price = request.GET.get('max', None)
    queryset = Item.objects.exclude(status=0)

    if item_name:
        queryset = queryset.filter(title__icontains=item_name)
    if category_id:
        queryset = queryset.filter(category=category_id)
    if art:
        queryset = queryset.filter(sku=art)
    if min_price:
        queryset = queryset.filter(price__gte=min_price)
    if max_price:
        queryset = queryset.filter(price__lte=max_price)

    return render(request, 'search.html', {'items': handle_pagination(request, queryset, 12), 'categories': categories})


def site_map(request):
    categories = Category.objects.order_by('name_en').all()
    return render(request, 'site_map.html', {'categories': categories})
