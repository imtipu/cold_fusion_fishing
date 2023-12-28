from django.contrib import admin

from .models import *


@admin.register(Project)
class ProejctAdmin(admin.ModelAdmin):
    list_display = ['title', 'tank', 'start_date', 'end_date', 'initial_quantity', 'display_total_dead',
                    'display_total_live', 'created_at',
                    'updated_at']
    autocomplete_fields = ['tank']
    search_fields = ['title', 'description']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related(
            'tank'
        ).annotate(
            total_dead=models.Sum('daily_activities__dead_fish', output_field=models.IntegerField(), default=0),
            total_live=models.F('initial_quantity') - models.F('total_dead'),
        )
        return queryset

    @admin.display(description='Total Dead')
    def display_total_dead(self, obj):
        if hasattr(obj, 'total_dead'):
            return obj.total_dead
        return None

    @admin.display(description='Total Live')
    def display_total_live(self, obj):
        if hasattr(obj, 'total_live'):
            return obj.total_live
        return None


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
