from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from product.forms import CommentForm
from product.models import Comment, Category
from product.utils import handle_pagination, queryset_with_locale


def open_detail(request, item_id):
    item = queryset_with_locale(request).filter(id=item_id).first()
    if not item:
        raise Http404
    items = queryset_with_locale(request).exclude(id=item_id)[:3]
    comments = Comment.objects.filter(item=item)
    form = CommentForm()

    return render(request, 'product/detail.html', {'item': item, 'items': items, 'comments': comments, 'form': form})


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


def category_list(request):
    categories = Category.objects.order_by('name_en').all()
    return render(request, 'home.html', {'categories': categories})


def category_detail(request, category_id):
    cat = get_object_or_404(Category, id=category_id)
    categories = Category.objects.order_by('name_en').all()

    if cat.sub_category.count() > 0:
        items = queryset_with_locale(request).filter(category__parent=cat)
    else:
        items = queryset_with_locale(request).filter(category__id=category_id)

    item = queryset_with_locale(request).filter(category__id=category_id).first()
    sub_categories = cat.sub_category.all()
    return render(request, 'product/category_detail.html', {'categories': categories,
                                                            'items': handle_pagination(request, items),
                                                            'cat': cat,
                                                            'item': item,
                                                            'sub_categories': sub_categories})

