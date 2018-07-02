from django.urls import path
from product import views

urlpatterns = [
    path('<int:item_id>/', views.open_detail, name='item-detail'),
    ]
