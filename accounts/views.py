from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import SignUpForm, LoginForm, ConfrimCode
from django.core.mail import EmailMessage
from random import randint
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.six import text_type
from django.contrib.auth import views
from django.urls import reverse_lazy
from . models import Profile

def register(request):
    global random_code, new_form
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        random_code = randint(1000, 9999)
        if form.is_valid():
            data = form.cleaned_data
            new_form = form.save(commit=False)

            email = EmailMessage(
                'authenticated',
                str(random_code),
                'activation code',
                [data['email']]
            )
            email.send(fail_silently=False)

            return redirect('confirm_code')

    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})


def confirm_email_code(request):
    if request.method == 'POST':
        form = ConfrimCode(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if random_code == data['code']:
                new_form.save()

                return redirect('login')


    else:
        form = ConfrimCode()
    return render(request, 'accounts/confrim_email_code.html', {'form': form})


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            try:
                user = authenticate(request, username=get_user_model().objects.get(email=data['user_name']),
                                    password=data['password'])
                messages.success(request, 'شما وارد حساب خود شدید')
            except:
                user = authenticate(request, username=data['user_name'],
                                    password=data['password'])
                messages.success(request, 'شما وارد حساب خود شدید')
            if user is not None:
                login(request, user)
                return redirect('product:products')

            else:
                messages.error(request, 'نام کاربری یا رمزعبور اشتباه است')


    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('product:products')




def profile_user(request):
    profile = Profile.objects.get(user_id=request.user.id)
    return render(request, 'accounts/profile.html', {'profile':profile})


class ResetPassword(views.PasswordResetView):
    template_name = 'accounts/reset_password.html'
    success_url = reverse_lazy('reset_done')
    email_template_name = 'accounts/email_template.html'


class DonePassword(views.PasswordResetDoneView):
    template_name = 'accounts/password_done.html'


class ConfirmPassword(views.PasswordResetConfirmView):
    template_name = 'accounts/password_confrim.html'
    success_url = reverse_lazy('complete')


class Complete(views.PasswordResetCompleteView):
    template_name = 'accounts/password_complate.html'







#
# class EmailToken(PasswordResetTokenGenerator):
#     def _make_hash_value(self, user, timestamp):
#         return (text_type(user.id) + text_type(timestamp))
#
# email_generator = EmailToken()
#
#
#
#         url = reverse('reset', kwargs={'uidb64':uidb64, "token": email_generator.make_token(user)})
#         domin = get_current_site(request).domain
#         uidb64 = urlsafe_base64_encode(force_bytes(user.id))
#         link = 'http//' + domain + url