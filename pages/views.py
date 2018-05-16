from django.shortcuts import render, get_object_or_404

from product.models import Item, Category


def home(request):
    items = Item.objects.all()[:12]
    categories = Category.objects.all()
    return render(request, 'home.html', {'items': items, 'categories': categories})


def about_us(request):
    return render(request, 'about_us.html')


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
        items = Item.objects.filter(category=query_category_id, title_en__icontains=query_item_name)
        return render(request, 'search.html', {'items': items, 'categories': categories, 'query_item_name':query_item_name, 'query_category_id':query_category_id})
    else:
        items = Item.objects.filter(title_en__icontains=query_item_name)
        return render(request, 'search.html', {'items': items, 'categories': categories, 'query_item_name':query_item_name})
