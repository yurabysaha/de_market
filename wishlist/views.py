import uuid

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from product.models import Item
from .models import Wishlist
from django.utils.translation import gettext as _


def add_to_wishlist(request, item_id):
    if not request.session.get('wishlist_id'):
        request.session['wishlist_id'] = str(uuid.uuid4())

    wishlist, created = Wishlist.objects.get_or_create(user_session=request.session['wishlist_id'])
    item = get_object_or_404(Item, id=item_id)
    wishlist.item.add(item)
    request.session['wishlist_count'] = wishlist.item.count()

    messages.success(request, _('You add item to Wish list!'))

    return redirect('/')


def remove_from_wishlist(request, item_id):
    if request.session.get('wishlist_id'):
        wishlist, created = Wishlist.objects.get_or_create(user_session=request.session['wishlist_id'])
        item = get_object_or_404(Item, id=item_id)
        wishlist.item.remove(item)

        if wishlist.item.count() != 0:
            request.session['wishlist_count'] = wishlist.item.count()
        else:
            del request.session['wishlist_count']

        return redirect('/wishlist')

    return redirect('/')


def get_wishlist(request):
    if not request.session.get('wishlist_id'):
        request.session['wishlist_id'] = str(uuid.uuid4())
    wishlist, created = Wishlist.objects.get_or_create(user_session=request.session['wishlist_id'])

    return render(request, 'wishlist/wishlist.html', {'wishlist': wishlist})
