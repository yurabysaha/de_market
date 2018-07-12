from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_order, name="create_order"),
    path('confirm/', views.confirm_order, name="confirm_order"),
    path('pay_upon_receipt/', views.pay_upon_receipt, name="pay_upon_receipt"),
]
