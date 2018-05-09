from django.shortcuts import render, get_object_or_404, redirect

from product.forms import CommentForm
from product.models import Comment, Item, Category


def open_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    items = Item.objects.exclude(id=item_id)[:3]
    comments = Comment.objects.all().filter(item=item)

    return render(request, 'product/detail.html', {'item': item, 'items': items, 'comments':comments})


def create_comment(request, item_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.user_id = request.user.id
                form.item_id = item_id
                form.save()
                return redirect('/item/{}'.format(item_id))
        else:
            form = CommentForm()
            return render(request, 'product/comment_create_update.html', {'form': form})
    else:
        return redirect('/')


def update_comment(request, comment_id, item_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=comment_id)
        if request.method == "POST":
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                return redirect('/item/{}'.format(item_id))
        else:
            form = CommentForm(instance=comment)
        return render(request, 'product/comment_create_update.html', {'form': form})
    else:
        return redirect('/')


def comment_delete(request, comment_id, item_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=comment_id)
        if request.method == "DELETE":
            comment.delete()
            return render(request, "product/detail.html")
        return render(request, "product/detail.html")
    else:
        return redirect('/')
