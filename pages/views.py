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
    query_item_name = request.GET.get('q')
    query_category_id = request.GET.get('category_id')
    if query_category_id:
        items = Item.objects.exclude(status=0).filter(category=query_category_id, title__icontains=query_item_name)
        return render(request, 'search.html', {'items': items, 'categories': categories, 'query_item_name':query_item_name, 'query_category_id':query_category_id})
    else:
        items = Item.objects.exclude(status=0).filter(title__icontains=query_item_name)
        return render(request, 'search.html', {'items': items, 'categories': categories, 'query_item_name':query_item_name})


def site_map(request):
    categories = Category.objects.order_by('name_en').all()
    return render(request, 'site_map.html', {'categories': categories})
