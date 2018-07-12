import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from product.models import Item


class Order(models.Model):
    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    ORDER_STATUS_CHOICES = (
        (0, _('New')),
        (1, _('Paid')),
        (2, _('Send to Client')),
    )

    PAYMENTS_METHOD_CHOICES = (
        (0, _('PayPal')),
        (1, _('Pay upon receipt')),
    )

    user_session = models.CharField(max_length=255, default=uuid.uuid4())
    items = models.ManyToManyField(Item, related_name='in_orders')
    track_number = models.CharField(max_length=255, verbose_name=_('Track Number'), blank=True)
    delivery_address = models.CharField(max_length=255, verbose_name=_('Delivery Address'), blank=True)
    contact_phone = models.CharField(max_length=255, verbose_name=_('Contact phone'), blank=True)
    status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_CHOICES[0][0])
    payment_method = models.IntegerField(choices=PAYMENTS_METHOD_CHOICES, null=True, verbose_name=_("Payment Method"))
    paid_by_paypal = models.BooleanField(default=False, verbose_name=_("Paid by PayPal"))
    total = models.IntegerField(verbose_name=_('Total price'), null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return _("Order # ") + str(self.pk)
