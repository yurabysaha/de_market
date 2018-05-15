from django.shortcuts import render, get_object_or_404, redirect

from product.forms import CommentForm
from product.models import Comment, Item, Category
from product.help_functions import handle_pagination

def open_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    items = Item.objects.exclude(id=item_id)[:3]

    return render(request, 'product/detail.html', {'item': item, 'items': items})


def create_comment(request, item_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.user_id = request.user_id
                form.item_id = item_id
                form.save()
                return redirect('item_details')
        else:
            form = CommentForm()
        return render(request, 'product/comment_create.html', {'form': form})
    else:
        return redirect('/')


def update_comment(request, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=comment_id)
        if request.method == "POST":
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                return redirect('item_details')
        else:
            form = CommentForm(instance=comment)
        return render(request, 'product/comment_edit.html', {'form': form})
    else:
        return redirect('/')


def comment_delete(request, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=comment_id)
        if request.method == "DELETE":
            comment.delete()
            return redirect("item_details")
        return render(request, "product/item_details.html")
    else:
        return redirect('/')


def category_list(request):
    categories = Category.objects.order_by('name_en').all()
    return render(request, 'home.html', {'categories': categories})


def category_detail(request, category_id):
    if request.method == "GET":
        cat = get_object_or_404(Category, id=category_id)
        categories = Category.objects.order_by('name_en').all()
        item_with_category = Item.objects.filter(category__id=category_id)
        item = Item.objects.filter(category__id=category_id)[0]
        return render(request, 'product/category_detail.html', {'categories': categories,
                                                                'item_with_category': handle_pagination(request, item_with_category),
                                                                'cat': cat,
                                                                'item': item })

