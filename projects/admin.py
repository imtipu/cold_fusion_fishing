from django.contrib import admin

from .models import *
from .utils import calculate_molas_to_add


@admin.register(Project)
class ProejctAdmin(admin.ModelAdmin):
    list_display = ['title', 'tank', 'start_date', 'end_date', 'initial_quantity', 'display_total_dead',
                    'display_total_live', 'expected_cn', 'undigested_percentage',
                    'created_at', 'updated_at']
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
    list_display = ['project', 'activity_date', 'dead_fish', 'display_molas_to_add',
                    'single_fish_weight', 'feed_percentage', 'display_expected_cn',
                    'created_at', 'updated_at']
    autocomplete_fields = ['project']
    search_fields = ['project__title']
    readonly_fields = [
        'total_live_fish',
        'display_molas_to_add'
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related(
            'project', 'project__tank', 'project__tank__current_project'
        ).annotate(
            initial_quantity=models.F('project__initial_quantity'),
            project_total_dead=models.Sum(
                'project__daily_activities__dead_fish',
                filter=models.Q(project__daily_activities__activity_date__lt=models.F('activity_date')),
                output_field=models.IntegerField(),
                default=0
            ),
            project_total_live=models.F('initial_quantity') - models.F('project_total_dead'),
            day_total_live=models.F('project_total_live') - models.F('dead_fish'),
        )
        return queryset

    @admin.display(description='Expected CN', ordering='expected_cn')
    def display_expected_cn(self, obj):
        return round(obj.expected_cn, 2)

    @admin.display(description='Molas to Add(gm)')
    def display_molas_to_add(self, obj):
        molas_to_add = calculate_molas_to_add(obj)
        return round(molas_to_add, 2)

    @admin.display(description='Day')
    def display_day(self, obj):
        return obj.day
