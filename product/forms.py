from django.forms import forms
from product.models import Comment


class CommentForm(forms.BaseForm):

    class Meta:
        model = Comment
        fields = ('user', 'body',)