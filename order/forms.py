from django import forms
from order.models import Order
from django.utils.translation import gettext_lazy as _


class CreateOrder(forms.Form):
    contact_phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label=_('Contact Phone'))
    delivery_address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}), label=_('Delivery Address'))

    class Meta:
        model = Order
        fields = ('delivery_address', 'contact_phone',)
