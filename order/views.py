from django.shortcuts import render, redirect
from . forms import CreateOrder
from cart.models import Cart
from . models import Order
from django.contrib import messages
from django.utils.translation import gettext as _


def create_order(request):
    if request.session.get('cart_id'):
        cart, created = Cart.objects.get_or_create(user_session=request.session['cart_id'])

        # calculate total for price in cart items
        cart_total = 0
        for i in cart.item.all():
            if i.sale_price:
                cart_total += i.sale_price
            else:
                cart_total += i.price

        form = CreateOrder()
        if request.method == "POST":
            order = Order.objects.create(user_session=request.session['cart_id'], total=cart_total,
                                         delivery_address=request.POST['delivery_address'],
                                         contact_phone=request.POST['contact_phone'])
            for item in cart.item.all():
                order.items.add(item)

            cart.item.clear()
            del request.session['cart_items_count']

            messages.info(request, _('Thank you for your order, our manager will contact you soon!'))

            return redirect('/')

        return render(request, 'order/order.html', {'form': form, 'cart':cart, 'cart_total':cart_total})

    else:
        return redirect('/')
