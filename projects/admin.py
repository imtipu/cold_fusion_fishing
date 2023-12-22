from django.contrib import admin

from .models import *


@admin.register(Project)
class ProejctAdmin(admin.ModelAdmin):
    list_display = ['title', 'tank', 'start_date', 'end_date', 'initial_quantity', 'created_at', 'updated_at']
    autocomplete_fields = ['tank']
    search_fields = ['title', 'description']


@admin.register(DailyActivity)
class DailyActivityAdmin(admin.ModelAdmin):
    list_display = ['project', 'activity_date', 'dead_fish', 'live_fish',
                    'single_fish_weight', 'feed_percentage', 'created_at',
                    'updated_at']
    autocomplete_fields = ['project']
    search_fields = ['project__title']
    readonly_fields = [
        'total_live_fish'
    ]
