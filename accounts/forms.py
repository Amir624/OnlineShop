from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import CustomUser, Profile
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime

error = {
    'required': 'این فیلد اجباری است',
    'invalid': 'درست وارد کنید',

}


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1',)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        del self.fields['password2']


class LoginForm(forms.Form):
    user_name = forms.CharField(max_length=50, error_messages=error)
    password = forms.CharField(widget=forms.PasswordInput, error_messages=error)


class ConfrimCode(forms.Form):
    code = forms.IntegerField()


class CompleteProfile(forms.ModelForm):
    birth_day = forms.DateField(widget=forms.TextInput(attrs={'placeholder': "به جای اسلش از خط فاصله استفاده کنید"}))
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'birth_day', 'mobile', 'address')

