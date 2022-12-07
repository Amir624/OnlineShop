from django.urls import path
from .views import register, log_in, confirm_email_code, log_out, ResetPassword, DonePassword, ConfirmPassword, \
    Complete, profile_user, profile_complete

urlpatterns = [
    path('signup/', register, name='signup'),
    path('login/', log_in, name='login'),
    path('confrim_code/', confirm_email_code, name='confirm_code'),
    path('logout/', log_out, name='logout'),
    path('reset/', ResetPassword.as_view(), name='reset'),
    path('reset/done/', DonePassword.as_view(), name='reset_done'),
    path('confrim/<uidb64>/<token>', ConfirmPassword.as_view(), name='password_reset_confirm'),
    path('confirm/done/', Complete.as_view(), name='complete'),
    path('profile/', profile_user, name='profile'),
    path('update/profile/', profile_complete, name='update_profile'),
]
