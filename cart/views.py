from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart
from product.models import Item


def add_to_cart(request, item_id):
    if request.user.is_authenticated:
        if request.method == "GET":
            cart, created = Cart.objects.get_or_create(user_id=request.user.id)
            item = get_object_or_404(Item, id=item_id)
            cart.item.add(item)
            messages.success(request, 'You add item to cart!')
    return redirect('/')


def remove_from_cart(request, item_id):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user_id=request.user.id)
        item = get_object_or_404(Item, id=item_id)
        cart.item.remove(item)
        return redirect('/cart')

    else:
        return redirect('/')


def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user_id=request.user.id)

        # canculate total for price in cart items
        cart_total = 0
        for i in cart.item.all():
            cart_total += i.price

        return render(request, 'cart.html', {'cart': cart, 'cart_total': cart_total})
    else:
        return redirect('/')
