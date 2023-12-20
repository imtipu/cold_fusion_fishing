from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from .models import *


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'date_joined']

    list_filter = ['is_staff', 'is_superuser', 'is_active', ]
    search_fields = ['username', 'first_name', 'last_name', 'email']
