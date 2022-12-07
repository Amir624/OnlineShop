from django import forms
from .models import Order


class FormOrder(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'phone', 'address', 'note')



class CouponForm(forms.Form):

    code = forms.CharField(max_length=50)

