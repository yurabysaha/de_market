from django.shortcuts import get_object_or_404
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

from order.models import Order


def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    print(ipn_obj.payment_status)
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the `business` field. (The user could tamper with
        # that fields on the payment form before it goes to PayPal)
        if ipn_obj.receiver_email != "feniks402@gmail.com":
            # Not a valid payment
            return
        order = get_object_or_404(Order, user_session=ipn_obj.invoice)

        if ipn_obj.mc_gross == order.total and ipn_obj.mc_currency == 'EUR':

            # mark the order as paid
            order.paid_by_paypal = True
            order.payment_method = 0
            order.save()
    else:
        return


valid_ipn_received.connect(show_me_the_money)
