from django import forms
from order.models import Order

class CreateOrder(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('delivery_address', 'contact_phone',)

        widgets = {
            'delivery_address': forms.TextInput(attrs={'class': 'text-area'}),
            'contact_phone': forms.TextInput(attrs={'class': 'text-area'}),
        }
