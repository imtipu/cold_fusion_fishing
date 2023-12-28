from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.admin.models import LogEntry
from .models import *

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['action_time', 'user', 'content_type', 'object_id', 'object_repr', 'action_flag', 'change_message']
    search_fields = ['object_repr', 'change_message']
    autocomplete_fields = ['user',]
    list_filter = ['action_flag', 'content_type', ]


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'date_joined']

    list_filter = ['is_staff', 'is_superuser', 'is_active', ]
    search_fields = ['username', 'first_name', 'last_name', 'email']
