from django.contrib import admin

from .models import *


@admin.register(FishTank)
class FishTankAdmin(admin.ModelAdmin):
    list_display = ['title', 'volume', 'is_active', 'created_at', 'updated_at']

    search_fields = ['title', 'volume', ]
    list_filter = ['is_active']
