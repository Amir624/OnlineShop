from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from products.models import Product, Variant
from .cart import Cart
from .forms import AddToCartProduct
from django.contrib import messages


def cart_view(request):
    cart = Cart(request)
    for item in cart:
        item['product_update_quantity_form'] = AddToCartProduct(initial={
            'quantity': item['quantity'],
            'inplace': True,
        })

    return render(request, 'cart/cart.html', {'cart': cart})


def add_to_cart(request, product_id):
    products = get_object_or_404(Variant, id=product_id)
    cart = Cart(request)

    form = AddToCartProduct(request.POST)
    if form.is_valid():
        cleaned_data = form.cleaned_data
        quantity = cleaned_data['quantity']
        cart.add(products, quantity, replace_current_quantity=cleaned_data['inplace'])
        messages.success(request, 'محصول به سبد خرید اضافه شد')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_cart(request, product_id):
    cart = Cart(request)

    products = get_object_or_404(Variant, id=product_id)

    cart.remove(products)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def clear_cart(request):
    cart = Cart(request)

    if len(cart):
        cart.clear()

    return redirect('product:products')