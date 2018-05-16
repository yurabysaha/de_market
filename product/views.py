from django.shortcuts import render, get_object_or_404, redirect
from product.forms import CommentForm
from product.models import Comment, Item, Category


def open_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    items = Item.objects.exclude(id=item_id)[:3]
    comments = Comment.objects.filter(item=item)
    form = CommentForm()
    if request.method == "POST":
        create_comment(request, item_id)
        return redirect('/item/{}'.format(item_id))
    else:
        return render(request, 'product/detail.html', {'item': item, 'items': items, 'comments': comments, 'form': form})


def create_comment(request, item_id):
    if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.user_id = request.user.id
                form.item_id = item_id
                form.save()
    else:
        return redirect('/')


def update_comment(request, comment_id, item_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=comment_id, user=request.user.id)
        if request.method == "POST":
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                return redirect('/item/{}'.format(item_id))
        else:
            form = CommentForm(instance=comment)
        return render(request, 'product/comment_update.html', {'form': form})
    else:
        return redirect('/')


def comment_delete(request, comment_id, item_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=comment_id, user=request.user.id)
        if request.method == "POST":
            comment.delete()
            return redirect('/item/{}'.format(item_id))
        return render(request, "product/detail.html")
    else:
        return redirect('/')
