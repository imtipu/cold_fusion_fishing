from django.contrib import admin

from .models import *


@admin.register(FishTank)
class FishTankAdmin(admin.ModelAdmin):
    list_display = ['title', 'capacity', 'volume', 'is_active', 'length', 'width', 'height', 'created_at',
                    'updated_at']

    search_fields = ['title', 'volume', 'length', 'width', 'height']
    list_filter = ['is_active']
