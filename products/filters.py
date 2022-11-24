import django_filters
from django import forms
from .models import *


class ProductFilter(django_filters.FilterSet):
    CHOICES = {
        ('گرانترین', 'گرانترین'),
        ('ارزان ترین', 'ارزان ترین'),
    }
    TIME_CHOICE = {
        ('جدیدترین', 'جدیدترین'),
        ('قدیمی ترین', 'قدیمی ترین'),

    }
    DISCOUNT = {
        ('بیشترین تخفیف', 'بیشترین تخفیف'),
        ('کم تخفیف','کم تخفیف'),
    }

    FAVORITE = {
        ('محبوب ترین', 'محبوب ترین'),
        ('کم محبوب','کم محبوب')
    }

    price1 = django_filters.NumberFilter(field_name='unit_price', lookup_expr='gte')
    price2 = django_filters.NumberFilter(field_name='unit_price', lookup_expr='lte')
    brand = django_filters.ModelMultipleChoiceFilter(queryset=Brand.objects.all(), widget=forms.CheckboxSelectMultiple)
    category = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all(),
                                                        widget=forms.CheckboxSelectMultiple)
    size = django_filters.ModelMultipleChoiceFilter(queryset=Size.objects.all(), widget=forms.CheckboxSelectMultiple)
    color = django_filters.ModelMultipleChoiceFilter(queryset=Color.objects.all(), widget=forms.CheckboxSelectMultiple)
    price = django_filters.ChoiceFilter(choices=CHOICES, method='price_filter')
    time_create = django_filters.ChoiceFilter(choices=TIME_CHOICE, method='time_filter')
    discount = django_filters.ChoiceFilter(choices=DISCOUNT, method='discount_filter', field_name='discount')
    total_favorite = django_filters.ChoiceFilter(choices=FAVORITE, method='filter_favorite', field_name='total_favorite')


    def price_filter(self, queryset, name, value):
        data = 'unit_price' if value == 'ارزان ترین' else '-unit_price'
        return queryset.order_by(data)

    def time_filter(self, queryset, name, value):
        data = 'time_create' if value == 'قدیمی ترین' else '-time_create'
        return queryset.order_by(data)

    def discount_filter(self, queryset, name, value):
        data = 'discount' if value ==  "کم تخفیف" else '-discount'
        return queryset.order_by(data)

    def filter_favorite(self,queryset, name, value):
        data = 'total_favorite' if value == 'محبوب ترین' else '-total_favorite'
        return queryset.order_by(data)
    