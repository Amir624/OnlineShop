from products.models import Product
from products.models import Variant
from orders.models import Coupon


class Cart:

    def __init__(self, request):
        self.request = request.user
        self.session = request.session
        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}
        self.coupon_id = self.session.get('coupon_id')
        self.cart = cart

    def add(self, product, quantity, replace_current_quantity=False):

        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}

        if replace_current_quantity:
            self.cart[product_id]['quantity'] = quantity

        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def remove(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):

        product_id = self.cart.keys()
        products = Variant.objects.filter(id__in=product_id)

        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product_obj'] = product

        for item in cart.values():
            item['total_price'] = item['product_obj'].unit_price * item['quantity']

            yield item

    def __len__(self):
        return len(self.cart.keys())

    def clear(self):
        del self.session['cart']
        self.save()

    def get_total_price(self):
        product_id = self.cart.keys()
        products = Variant.objects.filter(id__in=product_id)

        return sum(item['quantity'] * item['product_obj'].total_price for item in self.cart.values())

    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / 100) * self.get_total_price()
        return int(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
