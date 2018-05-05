from django.shortcuts import render, get_object_or_404, redirect
from product.models import Item
from .models import Wishlist


def add_to_wishlist(request, item_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            wishlist = Wishlist.objects.get_or_create(user_id=request.user.id)
            item = get_object_or_404(Item, id=item_id)
            wishlist = list(wishlist)
            wishlist.append(item)
            return render(request, 'wishlist/wishlist.html', {'wishlist': wishlist})

        else:
            return redirect('/wishlist')

    else:
        return redirect('/')


def remove_from_wishlist(request, item_id):
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.get_or_create(user_id=request.user.id)
        item = get_object_or_404(Item, id=item_id)
        wishlist = list(wishlist)
        wishlist.remove(item)
        return render(request, 'wushlist/wishlist.html', {'wishlist': wishlist})

    else:
        return redirect('/')


def get_wishlist(request):
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.get_or_create(user_id=request.user.id)
        return render(request, 'wishlist/wishlist.html', {'wishlist': wishlist})

    else:
        return redirect('/')
