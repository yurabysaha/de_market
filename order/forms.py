from django import forms
from order.models import Order

class CreateOrder(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('delivery_address', 'contact_phone',)
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

