from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart
from product.models import Item


def add_to_cart(request, item_id):
    if request.user.is_authenticated:

        if request.method == "POST":
            cart = Cart.objects.get_or_create(user_id=request.user_id)
            item = get_object_or_404(id=item_id)
            cart.add(item)
            return render(request, 'cart.html', {'cart': cart})
        else:
            return redirect('/cart')

    else:
        return redirect('/')


def remove_from_cart(request, item_id):
    if request.user.is_authenticated:
        cart = Cart.objects.get_or_create(user_id=request.user_id)
        item = get_object_or_404(id=item_id)
        cart.remove(item)
        return render(request, 'cart.html', {'cart': cart})

    else:
        return redirect('/')


def get_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get_or_create(user_id=request.user_id)
        return render(request, 'cart.html', {'cart': cart})

    else:
        return redirect('/')

