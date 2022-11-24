from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import CustomUser
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
