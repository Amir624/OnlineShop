from django.urls import path
from .views import *


urlpatterns=[
    path('', cart_view, name='cart'),
    path('add/cart/<int:product_id>/', add_to_cart, name='add_cart'),
    path('remove/cart/<int:product_id>/', remove_cart, name='remove_cart'),
    path('clear/cart/', clear_cart, name='clear_cart'),

]
