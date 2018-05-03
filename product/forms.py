from django.forms import forms
from product.models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('user', 'body',)