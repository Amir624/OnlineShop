from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['order', 'product', 'quantity', 'price', ]
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_paid')
    inlines = [
        OrderItemInline,
    ]


@admin.register(OrderItem)
class AdminItemOrder(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price',)
# Register your models here.
