from django.shortcuts import render, get_object_or_404, redirect
from product.models import Item
from .models import Wishlist


def add_to_wishlist(request, item_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            wishlist = Wishlist.objects.get_or_create(user_id=request.user_id)
            item = get_object_or_404(id=item_id)
            wishlist.add(item)
            return render(request, 'wishlist.html', {'wishlist': wishlist})
        else:
            return redirect('/wishlist')

    else:
        return redirect('/')


def remove_from_wishlist(request, item_id):
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.get_or_create(user_id=request.user_id)
        item = get_object_or_404(id=item_id)
        wishlist.remove(item)
        return render(request, 'wishlist.html', {'wishlist': wishlist})

    else:
        return redirect('/')


def get_wishlist(request):
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.get_or_create(user_id=request.user.id)
        return render(request, 'wishlist.html', {'wishlist': wishlist})

    else:
        return redirect('/')
