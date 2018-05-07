from django.shortcuts import render

from product.models import Item, Category


def home(request):
    items = Item.objects.all()[:12]
    categories = Category.objects.all()
    return render(request, 'home.html', {'items': items, 'categories': categories})


def about_us(request):
    return render(request, 'about_us.html')


def delivery(request):
    return render(request, 'delivery.html')


def faq(request):
    return render(request, 'faq.html')


def search(request):
    query = request.GET.get('q')
    items = Item.objects.filter(title_en__icontains=query)
    return render(request, 'search.html', {'items': items})
