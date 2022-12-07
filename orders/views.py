from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem, Coupon
from django.contrib import messages
from .forms import FormOrder, CouponForm
from cart.cart import Cart
from django.utils import timezone


def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, 'سبد خرید شما خالی است')

        return redirect('product:products')
    order_form = FormOrder()
    if request.method == 'POST':
        order_form = FormOrder(request.POST)
        if order_form.is_valid():
            order_obj = order_form.save(commit=False)
            order_obj.user = request.user
            order_obj.save()

            for item in cart:
                product = item['product_obj']
                order = OrderItem.objects.create(
                    product=product,
                    order=order_obj,
                    quantity=item['quantity'],
                    price=product.unit_price,
                )
            cart.clear()
            messages.success(request, 'سفارش شما ثبت شد')

            return redirect('product:products')

    return render(request, 'orders/order_create.html', {'form': order_form})


def order_detail(request, order_id):
    order = OrderItem.objects.get(id=order_id)
    return render(request, 'orders/order_details.html', {'order': order})


def coupon_apply(request):
    form = CouponForm()
    time = timezone.now()
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data
            try:
                coupon = Coupon.objects.get(code__exact=code['code'], start__lt=time, end__gt=time, active=True)
                request.session['coupon_id'] = coupon.id

            except Coupon.DoesNotExist:
                messages.error(request, 'کد تخفیف وجود ندارد')
                request.session['coupon_id'] = None
                return redirect('cart')

        return redirect('cart')
