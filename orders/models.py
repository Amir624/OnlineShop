from django.db import models
from products.models import Variant
from django.contrib.auth import get_user_model



class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.TextField()
    note = models.TextField(blank=True)
    phone = models.PositiveIntegerField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    datetime_create = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    discount = models.PositiveIntegerField(blank=True, null=True)

    def get_total_price(self):
        total = sum(i.get_price() for i in self.order_item.all())
        if self.discount :
            discount_price = (self.discount / 100) * total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_item')
    product = models.ForeignKey(Variant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()

    def get_price(self):
        return self.product.total_price * self.quantity


class Coupon(models.Model):
    code = models.CharField(max_length=50)
    start = models.DateTimeField()
    end = models.DateTimeField()
    discount = models.PositiveIntegerField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.code