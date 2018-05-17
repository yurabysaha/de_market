from django import forms
from order.models import Order


class CreateOrder(forms.Form):
    contact_phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    delivery_address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))

    class Meta:
        model = Order
        fields = ('delivery_address', 'contact_phone',)
