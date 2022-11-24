from django.urls import path
from .views import *

app_name = 'product'

urlpatterns = [
    path('', home_page, name='home'),
    path('products/', products_views, name='products'),
    path('product/details/<slug>/<int:pk>/', product_detail, name='detail_page'),
    path('comment/<int:pk>/', product_comments, name='comment'),
    path('comment/like/<int:pk>', comment_like, name='comment_like'),
    path('comment/dislike/<int:pk>', comment_dislike, name='comment_dislike'),
    path('favorite/product/<int:pk>', favorite_products, name='add_favorite_product'),
    path('remove/favorite/product/<int:pk>', remove_favorite_products, name='remove_favorite_product'),
    path('wish/list/', view_favorite_product, name='wish_list'),
    path('search/', search_bar, name='search'),
    path('compair/', compair_detail_view, name='compair'),
    path('add/compair/<int:product_id>/', add_to_compair, name='add_compair'),
    path('remove/compair/<int:product_id>/', remove_compair, name='remove_compair'),
]
