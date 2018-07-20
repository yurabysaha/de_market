from django.db.models import Q, Prefetch
from django.shortcuts import render

from product.models import Category, Item, ItemPhoto
from product.utils import handle_pagination


def home(request):
    items = Item.objects.exclude(status=0).prefetch_related(Prefetch('photos', queryset=ItemPhoto.objects.order_by('id')))
    categories = Category.objects.all().prefetch_related('sub_category')
    return render(request, 'pages/home.html', {'items': handle_pagination(request, items, 12), 'categories': categories})


def about_us(request):
    categories = Category.objects.all()
    return render(request, 'pages/about_us.html', {'categories': categories})


def delivery(request):
    categories = Category.objects.all()
    return render(request, 'pages/delivery.html', {'categories': categories})


def search(request):
    categories = Category.objects.all()
    item_name = request.GET.get('q', None)
    category_id = request.GET.getlist('qcategory', None)
    min_price = request.GET.get('min', None)
    max_price = request.GET.get('max', None)
    queryset = Item.objects.exclude(status=0).prefetch_related(Prefetch('photos', queryset=ItemPhoto.objects.order_by('id')))

    if item_name:
        queryset = queryset.filter(Q(title__icontains=item_name) | Q(sku=item_name))
    if category_id:
        queryset = queryset.filter(category__in=category_id)
    if min_price:
        queryset = queryset.filter(price__gte=min_price)
    if max_price:
        queryset = queryset.filter(price__lte=max_price)

    return render(request, 'pages/search.html', {'items': handle_pagination(request, queryset, 12), 'categories': categories, 'selected': category_id})
