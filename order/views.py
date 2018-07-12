from django.shortcuts import render, redirect
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm

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
            cart.delete()

            del request.session['cart_items_count']
            request.session['order_id'] = request.session['cart_id']
            del request.session['cart_id']

            return redirect('confirm_order')

        return render(request, 'order/order.html', {'form': form, 'cart': cart, 'cart_total': cart_total})

    else:
        return redirect('/')


def confirm_order(request):
    if request.session.get('order_id'):
        order = Order.objects.get(user_session=request.session['order_id'])

        # calculate total for price in cart items
        order_total = 0
        for i in order.items.all():
            if i.sale_price:
                order_total += i.sale_price
            else:
                order_total += i.price

        # What you want the button to do.
        paypal_dict = {
            "business": "feniks402@gmail.com",
            "amount": order_total,
            "currency_code": "EUR",
            "item_name": "name of the item",
            "invoice": request.session['order_id'],
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return": request.build_absolute_uri(reverse('create_order')),
            "cancel_return": request.build_absolute_uri(reverse('create_order')),
        }

        # Create the instance.
        paypal_form = PayPalPaymentsForm(initial=paypal_dict)

        return render(request, 'order/confirm_order.html', {'paypal_form': paypal_form, 'order': order, 'order_total': order_total})

    else:
        return redirect('/')


def pay_upon_receipt(request):
    if request.session.get('order_id'):
        order = Order.objects.get(user_session=request.session['order_id'])
        order.payment_method = 1
        order.save()

        del request.session['order_id']

        messages.info(request, _('Thank you for your order, our manager will contact you soon!'))

    return redirect('/')
