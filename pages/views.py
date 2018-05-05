from django.shortcuts import render

from product.models import Item, Category


def home(request):
    products = Item.objects.all()
    categories = Category.objects.all()
    return render(request, 'home.html', {'products': products, 'categories': categories})


def about_us(request):
    return render(request, 'about_us.html')


def delivery(request):
    return render(request, 'delivery.html')


def faq(request):
    return render(request, 'faq.html')
