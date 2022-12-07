from django.urls import path
from .views import order_create, coupon_apply, order_detail

urlpatterns = [
    path('', order_create, name='order'),
    path('order/detail/<int:order_id>/', order_detail, name='order_detail'),
    path('coupon/', coupon_apply, name='coupon'),
]