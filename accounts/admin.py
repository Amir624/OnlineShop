from django.contrib import admin
from .models import CustomUser, Profile
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin


@admin.register(Profile)
class ProfileAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'mobile',)


@admin.register(CustomUser)
class UserAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('username', 'email',)
