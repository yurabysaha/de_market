import uuid

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from .models import Cart
from product.models import Item
from django.utils.translation import gettext as _


def add_to_cart(request, item_id):
        if request.method == "GET":
            if not request.session.get('cart_id'):
                request.session['cart_id'] = str(uuid.uuid4())
            cart, created = Cart.objects.get_or_create(user_session=request.session['cart_id'])
            item = get_object_or_404(Item, id=item_id)
            cart.item.add(item)
            request.session['cart_items_count'] = cart.item.count()
            messages.success(request, _('You add item to cart!'))
        return redirect('/')


def remove_from_cart(request, item_id):
    if request.session.get('cart_id'):
        cart, created = Cart.objects.get_or_create(user_session=request.session['cart_id'])
        item = get_object_or_404(Item, id=item_id)
        cart.item.remove(item)
        if cart.item.count() != 0:
            request.session['cart_items_count'] = cart.item.count()
        else:
            del request.session['cart_items_count']

        return redirect('/cart')

    return redirect('/')


def get_cart(request):
    if request.session.get('cart_id'):
        cart, created = Cart.objects.get_or_create(user_session=request.session['cart_id'])

        # calculate total for price in cart items
        cart_total = 0
        for i in cart.item.all():
            if i.sale_price:
                cart_total += i.sale_price
            else:
                cart_total += i.price

        return render(request, 'cart/cart.html', {'cart': cart, 'cart_total': cart_total})

    return redirect('/')
