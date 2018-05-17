from django.shortcuts import render, get_object_or_404, redirect
from . forms import CreateOrder
from cart.models import Cart
from . models import Order
from cart.views import remove_from_cart
from django.contrib import messages


def create_order(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user_id=request.user.id)

        # calculate total for price in cart items
        cart_total = 0
        for i in cart.item.all():
            if i.sale_price:
                cart_total += i.sale_price
            else:
                cart_total += i.price

        form = CreateOrder()
        if request.method == "POST":
            items_in_cart = cart.item.all()
            order = Order.objects.create(user=request.user, total=cart_total,
                                         delivery_address=request.POST['delivery_address'],
                                         contact_phone=request.POST['contact_phone'])
            for item in items_in_cart:
                order.items.add(item)

            cart.item.clear()
            messages.info(request, 'Thank you for your order, our manager will contact you soon!')

            return redirect('/')

        return render(request, 'order/order.html', {'form': form, 'cart':cart, 'cart_total':cart_total})

    else:
        return redirect('/')
