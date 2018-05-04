from django.shortcuts import render, get_object_or_404, redirect

from product.forms import CommentForm
from product.models import Comment, Item


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
