# users/admin.py

from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'phone_number', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff')

admin.site.register(CustomUser, CustomUserAdmin)
