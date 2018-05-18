from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from product.models import Item
from product.utils import queryset_with_locale
from .models import Wishlist
from django.utils.translation import gettext as _


def add_to_wishlist(request, item_id):
    if request.user.is_authenticated:
        if request.method == "GET":
            wishlist, created = Wishlist.objects.get_or_create(user_id=request.user.id)
            item = get_object_or_404(Item, id=item_id)
            wishlist.item.add(item)
            messages.success(request, _('You add item to Wish list!'))

            return redirect('/')
    else:
        messages.info(request, _('Please login or register first!'))

    return redirect('/')


def remove_from_wishlist(request, item_id):
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user_id=request.user.id)
        item = get_object_or_404(Item, id=item_id)
        wishlist.item.remove(item)

        return redirect('/wishlist')
    else:
        return redirect('/')


def get_wishlist(request):
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user_id=request.user.id)
        item_in_wishlist = queryset_with_locale(request).filter(wishlist=wishlist)

        return render(request, 'wishlist/wishlist.html', {'wishlist': wishlist, 'item_in_wishlist': item_in_wishlist})
    else:
        messages.info(request, _('Please login or register first!'))
        return redirect('/')
