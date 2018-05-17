from django.shortcuts import render, get_object_or_404


def create_order(request):

    return render(request, 'order/order.html')